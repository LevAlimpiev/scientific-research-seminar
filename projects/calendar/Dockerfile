FROM golang:1.21-alpine

WORKDIR /app

# Установка зависимостей и PostgreSQL клиента
RUN apk add --no-cache postgresql-client

# Копирование скрипта ожидания
COPY scripts/wait-for-postgres.sh /wait-for-postgres.sh
RUN chmod +x /wait-for-postgres.sh

# Установка зависимостей Go
COPY go.mod ./
RUN go mod download

# Копирование исходного кода
COPY . .

# Сборка приложения
RUN go build -o main ./cmd/calendar

EXPOSE 8080

CMD ["/wait-for-postgres.sh", "db", "./main"]