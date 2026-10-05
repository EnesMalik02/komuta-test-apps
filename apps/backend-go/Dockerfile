FROM golang:1.25-alpine AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /out/api ./cmd/api

FROM alpine:3.21
RUN apk add --no-cache ca-certificates && adduser -D -u 10001 app
COPY --from=build /out/api /usr/local/bin/api
USER 10001
ENV PORT=8080
EXPOSE 8080
CMD ["api"]
