package models

import (
	"errors"
	"time"
)

var ErrEventNotFound = errors.New("event not found")

type Event struct {
	ID          int64     `json:"id"`
	CreatedBy   string    `json:"created_by"`
	CreatedAt   time.Time `json:"created_at"`
	Title       string    `json:"title"`
	Description string    `json:"description"`
	EventTime   time.Time `json:"event_time"`
	RemindAt    time.Time `json:"remind_at"`
}

type EventRepository interface {
	Create(event *Event) error
	Update(event *Event) error
	Delete(id int64) error
	GetAll() ([]Event, error)
	GetByID(id int64) (*Event, error)
}
