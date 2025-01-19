package main

import (
	"log"
	"net/http"
	"os"

	"calendar/handlers"
	"calendar/repository"

	"github.com/gorilla/mux"
)

func main() {
	// Получаем строку подключения к PostgreSQL из переменной окружения
	connStr := os.Getenv("DATABASE_URL")
	if connStr == "" {
		connStr = "postgres://postgres:postgres@localhost:5432/calendar?sslmode=disable"
	}

	// Инициализируем репозиторий
	repo, err := repository.NewPostgresRepository(connStr)
	if err != nil {
		log.Fatal(err)
	}

	// Инициализируем обработчик
	handler := handlers.NewEventHandler(repo)

	// Создаем маршрутизатор
	r := mux.NewRouter()

	// Определяем маршруты
	r.HandleFunc("/events", handler.CreateEvent).Methods("POST")
	r.HandleFunc("/events/{id}", handler.UpdateEvent).Methods("PUT")
	r.HandleFunc("/events/{id}", handler.DeleteEvent).Methods("DELETE")
	r.HandleFunc("/events", handler.GetAllEvents).Methods("GET")
	r.HandleFunc("/events/{id}", handler.GetEvent).Methods("GET")

	// Запускаем сервер
	log.Println("Server is running on http://localhost:8080")
	if err := http.ListenAndServe(":8080", r); err != nil {
		log.Fatal(err)
	}
}
