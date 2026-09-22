package config

import "os"

type Config struct {
	Port        string
	DatabaseURL string
	ValkeyURL   string
	RabbitMQURL string
}

func Load() Config {
	return Config{
		Port:        getEnv("PORT", "8080"),
		DatabaseURL: getEnv("DATABASE_URL", ""),
		ValkeyURL:   getEnv("VALKEY_URL", ""),
		RabbitMQURL: getEnv("RABBITMQ_URL", ""),
	}
}

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
