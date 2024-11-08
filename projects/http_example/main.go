package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"path/filepath"
)

const FILE_DIR = "./files"

// Обработчик GET-запросов – чтение файла
func handleGet(w http.ResponseWriter, r *http.Request) {
	filePath := filepath.Join(FILE_DIR, r.URL.Path[1:])
	data, err := ioutil.ReadFile(filePath) // Чтение содержимого файла
	if err != nil {
		http.Error(w, "Файл не найден", http.StatusNotFound)
		return
	}

	w.WriteHeader(http.StatusOK)
	w.Write(data)
}

// Обработчик POST-запросов – создание нового файла
func handlePost(w http.ResponseWriter, r *http.Request) {
	fmt.Println("In handlePost")
	filePath := filepath.Join(FILE_DIR, r.URL.Path[1:])

	// Проверяем, что файл уже не существует
	if _, err := os.Stat(filePath); err == nil {
		http.Error(w, "Файл уже существует", http.StatusConflict)
		return
	}

	data, err := ioutil.ReadAll(r.Body) // Чтение содержимого из тела запроса
	if err != nil {
		http.Error(w, "Произошла ошибка при чтении данных", http.StatusBadRequest)
		return
	}

	err = ioutil.WriteFile(filePath, data, 0644) // Запись файла
	if err != nil {
		http.Error(w, "Ошибка при создании файла", http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusCreated)
	fmt.Fprintln(w, "Файл создан")
}

// Обработчик PUT-запросов – обновление существующего файла
func handlePut(w http.ResponseWriter, r *http.Request) {
	fmt.Println("In handlePut")
	filePath := filepath.Join(FILE_DIR, r.URL.Path[1:])
	data, err := ioutil.ReadAll(r.Body) // Чтение содержимого из тела запроса
	if err != nil {
		http.Error(w, "Произошла ошибка при чтении данных", http.StatusBadRequest)
		return
	}

	err = ioutil.WriteFile(filePath, data, 0644) // Обновление файла
	if err != nil {
		http.Error(w, "Ошибка при обновлении файла", http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
	fmt.Fprintln(w, "Файл обновлен")
}

// Обработчик DELETE-запросов – удаление файла
func handleDelete(w http.ResponseWriter, r *http.Request) {
	filePath := filepath.Join(FILE_DIR, r.URL.Path[1:])

	// Проверяем наличие файла
	if _, err := os.Stat(filePath); os.IsNotExist(err) {
		http.Error(w, "Файл не существует", http.StatusNotFound)
		return
	}

	err := os.Remove(filePath) // Удаление файла
	if err != nil {
		http.Error(w, "Ошибка при удалении файла", http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
	fmt.Fprintln(w, "Файл удален")
}

func fileHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet:
		handleGet(w, r)
	case http.MethodPost:
		handlePost(w, r)
	case http.MethodPut:
		handlePut(w, r)
	case http.MethodDelete:
		handleDelete(w, r)
	default:
		http.Error(w, "Метод не поддерживается", http.StatusMethodNotAllowed)
	}
}

func main() {
	// Создаем директорию для хранения файлов, если она не существует
	if _, err := os.Stat(FILE_DIR); os.IsNotExist(err) {
		err := os.Mkdir(FILE_DIR, 0755)
		if err != nil {
			fmt.Println("Ошибка при создании директории:", err)
			return
		}
	}

	http.HandleFunc("/", fileHandler)
	fmt.Println("Сервер запущен на http://localhost:8082")
	err := http.ListenAndServe(":8082", nil)
	if err != nil {
		fmt.Println("Ошибка при запуске сервера:", err)
	}
}
