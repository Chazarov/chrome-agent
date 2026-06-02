package main

import (
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strings"

	"github.com/jmoiron/sqlx"
	"github.com/sirupsen/logrus"
)

func runMigrations(db *sqlx.DB) error {

	// Получаем путь к папке с миграциями
	migrationsDir := "migrations"

	// Читаем все файлы миграций
	files, err := filepath.Glob(filepath.Join(migrationsDir, "*.sql"))
	if err != nil {
		return fmt.Errorf("ошибка чтения папки миграций: %w", err)
	}

	sort.Strings(files)

	for _, file := range files {
		fileName := filepath.Base(file)
		migrationName := strings.TrimSuffix(fileName, ".sql")

		// Читаем содержимое файла миграции
		content, err := os.ReadFile(file)
		if err != nil {
			return fmt.Errorf("ошибка чтения файла миграции %s: %w", file, err)
		}

		// Применяем миграцию
		_, err = db.Exec(string(content))
		if err != nil {
			return fmt.Errorf("ошибка применения миграции %s: %w", migrationName, err)
		}

	}

	logrus.Println("Все миграции успешно применены")
	return nil
}

func initDB(cfg Config) (*sqlx.DB, error) {
	dsn := fmt.Sprintf("host=%s port=%s user=%s dbname=%s sslmode=%s search_path=%s,public",
		cfg.DB.Host,
		cfg.DB.Port,
		cfg.DB.Username,
		cfg.DB.DBName,
		cfg.DB.SSLMode,
		cfg.DB.Schema,
	)

	if cfg.DB.Password != "" {
		dsn += " password=" + cfg.DB.Password
	}

	db, err := sqlx.Connect("postgres", dsn)
	if err = db.Ping(); err != nil {
		return nil, err
	}
	return db, nil
}
