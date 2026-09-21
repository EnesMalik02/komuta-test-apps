package main

import (
	"context"
	"log"
	"net/http"

	amqp "github.com/rabbitmq/amqp091-go"
	"komuta-test-apps/backend-go/internal/cache"
	"komuta-test-apps/backend-go/internal/config"
	"komuta-test-apps/backend-go/internal/db"
	"komuta-test-apps/backend-go/internal/httpapi"
	"komuta-test-apps/backend-go/internal/queue"
)

func main() {
	cfg := config.Load()
	ctx := context.Background()

	pool, err := db.Connect(ctx, cfg.DatabaseURL)
	if err != nil {
		log.Fatalf("postgres connect: %v", err)
	}
	defer pool.Close()

	rdb, err := cache.Connect(ctx, cfg.ValkeyURL)
	if err != nil {
		log.Fatalf("valkey connect: %v", err)
	}
	defer rdb.Close()

	// RabbitMQ addon still provisioning on Komuta — wire back in once RABBITMQ_URL is set.
	var conn *amqp.Connection
	if cfg.RabbitMQURL != "" {
		conn, err = queue.Connect(cfg.RabbitMQURL)
		if err != nil {
			log.Fatalf("rabbitmq connect: %v", err)
		}
		defer conn.Close()
	}

	srv := &httpapi.Server{DB: pool, Cache: rdb, Queue: conn}

	log.Printf("backend-go listening on :%s", cfg.Port)
	if err := http.ListenAndServe(":"+cfg.Port, httpapi.NewRouter(srv)); err != nil {
		log.Fatal(err)
	}
}
