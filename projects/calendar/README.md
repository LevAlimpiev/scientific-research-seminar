# Calendar Service

Сервис для управления событиями календаря с использованием Go и PostgreSQL.

## Требования

- Docker
- Docker Compose

## Запуск приложения

1. Клонируйте репозиторий
2. Перейдите в директорию проекта
3. Запустите приложение:

```bash
docker-compose up --build
```

Сервис будет доступен по адресу: http://localhost:8080

## Тестирование

В проекте реализовано два типа тестов:

### Модульные тесты (Unit Tests)
Тестируют компоненты в изоляции, используя моки:
```bash
docker-compose -f docker-compose.test.yml up unit-test --abort-on-container-exit
```

### Функциональные тесты (Functional Tests)
Тестируют полный жизненный цикл API:
```bash
docker-compose -f docker-compose.test.yml up functional-test --abort-on-container-exit
```

### Запуск всех тестов
Для запуска всех тестов используйте:
```bash
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

## Структура проекта

- `cmd/` - исполняемые приложения
  - `calendar/` - основное приложение календаря
- `models/` - модели данных
- `handlers/` - HTTP обработчики
- `repository/` - слой доступа к данным
- `tests/`
  - `ut/` - модульные тесты
  - `ft/` - функциональные тесты
- `init.sql` - скрипт инициализации базы данных
- `Dockerfile` - конфигурация для сборки приложения
- `Dockerfile.test` - конфигурация для запуска тестов
- `docker-compose.yml` - конфигурация для запуска приложения
- `docker-compose.test.yml` - конфигурация для запуска тестов

## API Endpoints

### Создание события
```bash
POST /events
Content-Type: application/json

{
    "created_by": "user123",
    "title": "Встреча",
    "description": "Важная встреча",
    "event_time": "2024-01-20T15:00:00Z",
    "remind_at": "2024-01-20T14:45:00Z"
}
```

### Получение всех событий
```bash
GET /events
```

### Получение события по ID
```bash
GET /events/{id}
```

### Обновление события
```bash
PUT /events/{id}
Content-Type: application/json

{
    "title": "Обновленная встреча",
    "description": "Обновленное описание",
    "event_time": "2024-01-20T16:00:00Z",
    "remind_at": "2024-01-20T15:45:00Z"
}
```

### Удаление события
```bash
DELETE /events/{id}
```