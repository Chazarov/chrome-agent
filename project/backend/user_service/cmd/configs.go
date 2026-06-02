package main

import (
	"github.com/Chazarov/simple-shop/project/backend/pkg/config/config_structs"
)

type PsqlDatabaseConfig struct {
	Host     string `env:"PSQL_DB_HOST"`
	Port     string `env:"PSQL_DB_PORT"`
	Username string `env:"PSQL_DB_USERNAME"`
	Password string `env:"PSQL_DB_PASSWORD"`
	DBName   string `env:"PSQL_DB_NAME"`
	SSLMode  string `env:"PSQL_DB_SSL_MODE"`
	Schema   string `env:"PSQL_DB_SCHEMA"`
}

type Config struct {
	BaseConfig config_structs.BaseConfig
	DB         PsqlDatabaseConfig
	JWT        config_structs.AuthConfig
	CORS       config_structs.CorsConfig
}
