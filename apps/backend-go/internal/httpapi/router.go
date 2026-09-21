package httpapi

import (
	"context"
	"encoding/json"
	"net/http"

	"github.com/jackc/pgx/v5/pgxpool"
	amqp "github.com/rabbitmq/amqp091-go"
	"github.com/redis/go-redis/v9"
)

type Server struct {
	DB     *pgxpool.Pool
	Cache  *redis.Client
	Queue  *amqp.Connection
}

func NewRouter(s *Server) http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /health", s.health)
	return withCORS(mux)
}

func withCORS(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		next.ServeHTTP(w, r)
	})
}

func (s *Server) health(w http.ResponseWriter, r *http.Request) {
	ctx := context.Background()
	status := map[string]string{"postgres": "ok", "valkey": "ok", "rabbitmq": "ok"}

	if err := s.DB.Ping(ctx); err != nil {
		status["postgres"] = err.Error()
	}
	if err := s.Cache.Ping(ctx).Err(); err != nil {
		status["valkey"] = err.Error()
	}
	if s.Queue == nil {
		status["rabbitmq"] = "disabled"
	} else if s.Queue.IsClosed() {
		status["rabbitmq"] = "closed"
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(status)
}
