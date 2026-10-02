package queue

import (
	"context"
	"log"
	"strconv"

	"github.com/jackc/pgx/v5/pgxpool"
	amqp "github.com/rabbitmq/amqp091-go"
	"github.com/redis/go-redis/v9"
)

const Name = "messages"

func Connect(url string) (*amqp.Connection, error) {
	return amqp.Dial(url)
}

// Consume marks each message processed in postgres and bumps a valkey counter.
// ponytail: no reconnect/retry; restart pod if the connection drops.
func Consume(conn *amqp.Connection, pool *pgxpool.Pool, rdb *redis.Client) error {
	ch, err := conn.Channel()
	if err != nil {
		return err
	}
	if _, err := ch.QueueDeclare(Name, true, false, false, false, nil); err != nil {
		return err
	}
	msgs, err := ch.Consume(Name, "", false, false, false, false, nil)
	if err != nil {
		return err
	}
	ctx := context.Background()
	for m := range msgs {
		id, err := strconv.Atoi(string(m.Body))
		if err != nil {
			m.Nack(false, false)
			continue
		}
		if _, err := pool.Exec(ctx, "UPDATE messages SET status='processed' WHERE id=$1", id); err != nil {
			log.Printf("update %d: %v", id, err)
			m.Nack(false, true)
			continue
		}
		rdb.Incr(ctx, "processed_count")
		m.Ack(false)
	}
	return nil
}
