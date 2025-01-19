package ft

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"testing"
	"time"

	"calendar/models"
)

var baseURL string

func TestMain(m *testing.M) {
	baseURL = os.Getenv("API_URL")
	if baseURL == "" {
		baseURL = "http://localhost:8080"
	}
	os.Exit(m.Run())
}

func TestEventLifecycle(t *testing.T) {
	// 1. Создание события
	event := models.Event{
		CreatedBy:   "ft_test_user",
		Title:       "Functional Test Event",
		Description: "Test Description",
		EventTime:   time.Now().Add(24 * time.Hour),
		RemindAt:    time.Now().Add(23 * time.Hour),
	}

	// Создаем событие
	body, _ := json.Marshal(event)
	resp, err := http.Post(fmt.Sprintf("%s/events", baseURL), "application/json", bytes.NewBuffer(body))
	if err != nil {
		t.Fatalf("Failed to create event: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusCreated {
		t.Fatalf("Expected status code %d, got %d", http.StatusCreated, resp.StatusCode)
	}

	var createdEvent models.Event
	json.NewDecoder(resp.Body).Decode(&createdEvent)

	// 2. Получение события
	resp, err = http.Get(fmt.Sprintf("%s/events/%d", baseURL, createdEvent.ID))
	if err != nil {
		t.Fatalf("Failed to get event: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		t.Fatalf("Expected status code %d, got %d", http.StatusOK, resp.StatusCode)
	}

	var retrievedEvent models.Event
	json.NewDecoder(resp.Body).Decode(&retrievedEvent)

	if retrievedEvent.Title != event.Title {
		t.Errorf("Expected title %s, got %s", event.Title, retrievedEvent.Title)
	}

	// 3. Обновление события
	retrievedEvent.Title = "Updated Functional Test Event"
	body, _ = json.Marshal(retrievedEvent)

	req, _ := http.NewRequest("PUT", fmt.Sprintf("%s/events/%d", baseURL, retrievedEvent.ID), bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err = client.Do(req)
	if err != nil {
		t.Fatalf("Failed to update event: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		t.Fatalf("Expected status code %d, got %d", http.StatusOK, resp.StatusCode)
	}

	// 4. Проверка обновления
	resp, err = http.Get(fmt.Sprintf("%s/events/%d", baseURL, retrievedEvent.ID))
	if err != nil {
		t.Fatalf("Failed to get updated event: %v", err)
	}
	defer resp.Body.Close()

	var updatedEvent models.Event
	json.NewDecoder(resp.Body).Decode(&updatedEvent)

	if updatedEvent.Title != "Updated Functional Test Event" {
		t.Errorf("Expected updated title %s, got %s", "Updated Functional Test Event", updatedEvent.Title)
	}

	// 5. Удаление события
	req, _ = http.NewRequest("DELETE", fmt.Sprintf("%s/events/%d", baseURL, retrievedEvent.ID), nil)
	resp, err = client.Do(req)
	if err != nil {
		t.Fatalf("Failed to delete event: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusNoContent {
		t.Fatalf("Expected status code %d, got %d", http.StatusNoContent, resp.StatusCode)
	}

	// 6. Проверка удаления
	resp, err = http.Get(fmt.Sprintf("%s/events/%d", baseURL, retrievedEvent.ID))
	if err != nil {
		t.Fatalf("Failed to check deleted event: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusNotFound {
		t.Errorf("Expected status code %d for deleted event, got %d", http.StatusNotFound, resp.StatusCode)
	}
}
