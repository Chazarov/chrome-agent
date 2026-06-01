package handler

import (
	spreadMiddleware "github.com/Chazarov/simple-shop/project/backend/pkg/adapters/api/v1/middleware"
	"github.com/Chazarov/simple-shop/project/backend/pkg/config/config_structs"
	"github.com/Chazarov/simple-shop/project/backend/pkg/logger"
	"github.com/Chazarov/simple-shop/project/backend/user_service/internal/domain/service"
	"github.com/Chazarov/simple-shop/project/backend/user_service/pkg/adapters/api/middleware"
	"github.com/Chazarov/simple-shop/project/backend/user_service/pkg/service/auth"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

type Handler struct {
	services                    *service.Service
	logger                      *logger.ContextLogger
	jwtService                  *auth.JWTService
	userAuthorizationMiddleware *middleware.UserAuthorizationMiddleware
	spreadMiddleware            *spreadMiddleware.SpreadMiddleware
}

func NewHandler(service *service.Service,
	logger *logger.ContextLogger,
	jwtService *auth.JWTService,
	userAuthorizationMiddleware *middleware.UserAuthorizationMiddleware,
	spreadMiddleware *spreadMiddleware.SpreadMiddleware) *Handler {
	return &Handler{services: service, logger: logger, jwtService: jwtService, userAuthorizationMiddleware: userAuthorizationMiddleware, spreadMiddleware: spreadMiddleware}
}

func (h *Handler) InitRoutes(corsConfig *config_structs.CorsConfig) *gin.Engine {
	router := gin.Default()

	// CORS middleware
	if corsConfig.CorsEnabled {
		corsConfigGin := cors.Config{
			AllowAllOrigins:  corsConfig.AllowAllOrigins,
			AllowOrigins:     corsConfig.AllowOrigins,
			AllowMethods:     corsConfig.AllowMethods,
			AllowHeaders:     corsConfig.AllowHeaders,
			AllowCredentials: corsConfig.AllowCredentials,
			ExposeHeaders:    corsConfig.ExposeHeaders,
		}
		router.Use(cors.New(corsConfigGin))
	}

	router.Use(h.spreadMiddleware.AddSpreadInContext())

	base := router.Group("/user")
	base.Use(h.userAuthorizationMiddleware.AddAccessTokenToContext())
	{
		base.GET("/me", h.GetCurrentUser)
		base.POST("/logout", h.Logout)
		base.POST("/refresh", h.RefreshTokens)
		base.DELETE("/me", h.DeleteAccount)
	}

	auth := router.Group("/auth")
	{
		auth.POST("/register", h.Register)
		auth.POST("/login", h.Login)
	}

	router.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{"status": "ok"})
	})

	return router
}
