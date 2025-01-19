package handlers_test

import (
	"bytes"
	"calendar/handlers"
	"calendar/models"
	"calendar/tests/ut/mocks"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/gorilla/mux"
)

func TestCreateEvent(t *testing.T) {
	mockRepo := mocks.NewMockRepository()
	handler := handlers.NewEventHandler(mockRepo)

	event := models.Event{
		CreatedBy:   "test_user",
		Title:       "Test Event",
		Description: "Test Description",
		EventTime:   time.Now().Add(24 * time.Hour),
		RemindAt:    time.Now().Add(23 * time.Hour),
	}

	body, _ := json.Marshal(event)
	req := httptest.NewRequest("POST", "/events", bytes.NewBuffer(body))
	w := httptest.NewRecorder()

	handler.CreateEvent(w, req)

	if w.Code != http.StatusCreated {
		t.Errorf("Expected status code %d, got %d", http.StatusCreated, w.Code)
	}

	var response models.Event
	json.Unmarshal(w.Body.Bytes(), &response)

	if response.ID == 0 {
		t.Error("Expected event ID to be set")
	}
}

func TestGetEvent(t *testing.T) {
	mockRepo := mocks.NewMockRepository()
	handler := handlers.NewEventHandler(mockRepo)

	// Создаем тестовое событие
	event := &models.Event{
		CreatedBy:   "test_user",
		CreatedAt:   time.Now(),
		Title:       "Test Event",
		Description: "Test Description",
		EventTime:   time.Now().Add(24 * time.Hour),
		RemindAt:    time.Now().Add(23 * time.Hour),
	}
	mockRepo.Create(event)

	req := httptest.NewRequest("GET", "/events/1", nil)
	w := httptest.NewRecorder()

	// Добавляем параметры маршрутизации
	vars := map[string]string{
		"id": "1",
	}
	req = mux.SetURLVars(req, vars)

	handler.GetEvent(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("Expected status code %d, got %d", http.StatusOK, w.Code)
	}

	var response models.Event
	json.Unmarshal(w.Body.Bytes(), &response)

	if response.Title != event.Title {
		t.Errorf("Expected title %s, got %s", event.Title, response.Title)
	}
}

func TestUpdateEvent(t *testing.T) {
	mockRepo := mocks.NewMockRepository()
	handler := handlers.NewEventHandler(mockRepo)

	// Создаем тестовое событие
	event := &models.Event{
		CreatedBy:   "test_user",
		CreatedAt:   time.Now(),
		Title:       "Test Event",
		Description: "Test Description",
		EventTime:   time.Now().Add(24 * time.Hour),
		RemindAt:    time.Now().Add(23 * time.Hour),
	}
	mockRepo.Create(event)

	// Обновляем событие
	event.Title = "Updated Event"
	body, _ := json.Marshal(event)
	req := httptest.NewRequest("PUT", "/events/1", bytes.NewBuffer(body))
	w := httptest.NewRecorder()

	vars := map[string]string{
		"id": "1",
	}
	req = mux.SetURLVars(req, vars)

	handler.UpdateEvent(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("Expected status code %d, got %d", http.StatusOK, w.Code)
	}

	var response models.Event
	json.Unmarshal(w.Body.Bytes(), &response)

	if response.Title != "Updated Event" {
		t.Errorf("Expected title %s, got %s", "Updated Event", response.Title)
	}
}

func TestDeleteEvent(t *testing.T) {
	mockRepo := mocks.NewMockRepository()
	handler := handlers.NewEventHandler(mockRepo)

	// Создаем тестовое событие
	event := &models.Event{
		CreatedBy:   "test_user",
		CreatedAt:   time.Now(),
		Title:       "Test Event",
		Description: "Test Description",
		EventTime:   time.Now().Add(24 * time.Hour),
		RemindAt:    time.Now().Add(23 * time.Hour),
	}
	mockRepo.Create(event)

	req := httptest.NewRequest("DELETE", "/events/1", nil)
	w := httptest.NewRecorder()

	vars := map[string]string{
		"id": "1",
	}
	req = mux.SetURLVars(req, vars)

	handler.DeleteEvent(w, req)

	if w.Code != http.StatusNoContent {
		t.Errorf("Expected status code %d, got %d", http.StatusNoContent, w.Code)
	}

	// Проверяем, что событие удалено
	events, _ := mockRepo.GetAll()
	if len(events) != 0 {
		t.Error("Expected events to be empty after deletion")
	}
}
