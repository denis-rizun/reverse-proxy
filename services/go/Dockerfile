FROM golang:1.24.4 AS builder

WORKDIR /app

COPY services/go/go.mod services/go/go.sum ./
RUN go mod download

COPY services/go/ .

RUN go build -o main ./src/cmd/proxy/main.go

FROM debian:bookworm-slim

WORKDIR /app

COPY --from=builder /app/main .
COPY services/go/config.yml .

EXPOSE 8000
EXPOSE 9090

ENTRYPOINT ["./main"]