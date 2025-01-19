package mocks

import (
	"calendar/models"
	"sync"
)

// MockRepository реализует интерфейс EventRepository для тестирования
type MockRepository struct {
	events map[int64]models.Event
	mutex  sync.RWMutex
	nextID int64
}

func NewMockRepository() *MockRepository {
	return &MockRepository{
		events: make(map[int64]models.Event),
		nextID: 1,
	}
}

func (m *MockRepository) Create(event *models.Event) error {
	m.mutex.Lock()
	defer m.mutex.Unlock()

	event.ID = m.nextID
	m.events[event.ID] = *event
	m.nextID++
	return nil
}

func (m *MockRepository) Update(event *models.Event) error {
	m.mutex.Lock()
	defer m.mutex.Unlock()

	if _, exists := m.events[event.ID]; !exists {
		return models.ErrEventNotFound
	}

	m.events[event.ID] = *event
	return nil
}

func (m *MockRepository) Delete(id int64) error {
	m.mutex.Lock()
	defer m.mutex.Unlock()

	if _, exists := m.events[id]; !exists {
		return models.ErrEventNotFound
	}

	delete(m.events, id)
	return nil
}

func (m *MockRepository) GetAll() ([]models.Event, error) {
	m.mutex.RLock()
	defer m.mutex.RUnlock()

	events := make([]models.Event, 0, len(m.events))
	for _, event := range m.events {
		events = append(events, event)
	}
	return events, nil
}

func (m *MockRepository) GetByID(id int64) (*models.Event, error) {
	m.mutex.RLock()
	defer m.mutex.RUnlock()

	event, exists := m.events[id]
	if !exists {
		return nil, models.ErrEventNotFound
	}
	return &event, nil
}
