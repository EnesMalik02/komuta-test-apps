FROM golang:1.25-alpine AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /out/app ./cmd/api

FROM alpine:3.22
WORKDIR /app
COPY --from=builder /out/app /app/app
ENV PORT=8080
EXPOSE 8080
USER 1001
CMD ["/app/app"]
