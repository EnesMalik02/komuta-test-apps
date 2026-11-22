FROM golang:1.25-alpine AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /out/api ./cmd/api

FROM alpine:3.22
WORKDIR /app
COPY --from=builder /out/api /app/api
ENV PORT=8080
EXPOSE 8080
USER 1001
CMD ["/app/api"]
