package app

import (
	"database/sql"
	"fmt"
	"log"
	database "marketplace/internal/database"
	service "marketplace/internal/service"
	handlers "marketplace/internal/transport/http"
	"net/http"

	_ "github.com/lib/pq"
)

func Run() {
	db, err := sql.Open("postgres", "user=postgres password=mysecretpassword dbname=marketplace sslmode=disable")

	if err != nil {
		log.Fatal("Failed to connect to the database:", err)
	}
	defer db.Close()

	dbAccesor := database.NewPostgresAccessor(db)
	service := service.NewService(dbAccesor)
	handler := handlers.NewHandlers(service)

	http.HandleFunc("/add_product", handler.AddProduct)
	http.HandleFunc("/dump", handler.DumpAllProducts)
	http.HandleFunc("/search_products", handler.SearchProducts)

	fmt.Println("Start http server :8082")
	err = http.ListenAndServe(":8082", nil)
	if err != nil {
		log.Fatal("err")
	}
}
