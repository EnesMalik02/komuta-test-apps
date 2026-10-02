FROM golang:1.25 AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /out/app ./cmd/api

FROM alpine:3.20
WORKDIR /app
RUN adduser -D -u 1001 appuser
COPY --from=builder /out/app /app/app
ENV PORT=8080
EXPOSE 8080
USER 1001
CMD ["/app/app"]
