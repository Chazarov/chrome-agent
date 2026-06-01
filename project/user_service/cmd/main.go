package main

import (
	"context"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	_ "github.com/lib/pq"

	spreadMiddleware "github.com/Chazarov/simple-shop/project/backend/pkg/adapters/api/v1/middleware"
	"github.com/Chazarov/simple-shop/project/backend/pkg/config"
	"github.com/Chazarov/simple-shop/project/backend/pkg/context/trace"
	"github.com/Chazarov/simple-shop/project/backend/pkg/logger"
	"github.com/Chazarov/simple-shop/project/backend/user_service/internal/adapters/api/handler"
	postgresRepository "github.com/Chazarov/simple-shop/project/backend/user_service/internal/adapters/repository/postgres"
	"github.com/Chazarov/simple-shop/project/backend/user_service/internal/domain/service"
	"github.com/Chazarov/simple-shop/project/backend/user_service/pkg/adapters/api/middleware"
	"github.com/Chazarov/simple-shop/project/backend/user_service/pkg/service/auth"
	"github.com/gin-gonic/gin"
)

func main() {
	gin.SetMode(gin.ReleaseMode)

	ctx := context.Background()
	ctx = trace.WithSpread(ctx, "user_service_init")
	logger := logger.NewContextLogger()
	configInitializer := config.NewConfigInitializer(logger)

	cfg := Config{}
	if err := configInitializer.InitConfig(ctx, &cfg); err != nil {
		logger.Fatalf(ctx, "ошибка инициализации конфигурации: %s", err.Error())
	}

	db, err := initDB(cfg)
	if err != nil {
		logger.Fatalf(ctx, "ошибка инициализации подключения к БД: %s", err.Error())
	}
	defer db.Close()
	if err := runMigrations(db); err != nil {
		logger.Fatalf(ctx, "ошибка применения миграций: %s", err.Error())
	}

	logger.Info(ctx, "cors origins: %v", cfg.CORS.AllowOrigins)
	userRepo := postgresRepository.NewUserRepository(db, logger)

	// Создаем JWT сервис
	jwtService := auth.NewJWTService(cfg.JWT.SecretKey, cfg.JWT.AccessTokenExpiresIn, cfg.JWT.RefreshTokenExpiresIn, logger)

	userService := service.NewUserService(userRepo, logger, jwtService)
	service := service.NewService(userService)

	userAuthorizationMiddleware := middleware.NewUserAuthorizationMiddleware(logger)
	spreadMiddleware := spreadMiddleware.NewSpreadMiddleware(logger)

	handler := handler.NewHandler(service, logger, jwtService, userAuthorizationMiddleware, spreadMiddleware)

	router := handler.InitRoutes(&cfg.CORS)

	srv := &http.Server{
		Addr:    cfg.BaseConfig.Host + ":" + cfg.BaseConfig.Port,
		Handler: router,
	}

	go func() {
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			logger.Fatalf(ctx, "ошибка запуска сервера: %s\n", err)
		}
	}()

	logger.Infof(ctx, "User Service запущен на %s:%s", cfg.BaseConfig.Host, cfg.BaseConfig.Port)

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	logger.Infof(ctx, "Остановка сервера...")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		logger.Fatalf(ctx, "Принудительная остановка сервера: %s", err)
	}

	logger.Infof(ctx, "Сервер остановлен")
}
