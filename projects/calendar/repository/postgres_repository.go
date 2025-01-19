package repository

import (
	"calendar/models"
	"database/sql"

	_ "github.com/lib/pq"
)

type PostgresRepository struct {
	db *sql.DB
}

func NewPostgresRepository(connStr string) (*PostgresRepository, error) {
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		return nil, err
	}

	err = db.Ping()
	if err != nil {
		return nil, err
	}

	return &PostgresRepository{db: db}, nil
}

func (r *PostgresRepository) Create(event *models.Event) error {
	query := `
		INSERT INTO events (created_by, created_at, title, description, event_time, remind_at)
		VALUES ($1, $2, $3, $4, $5, $6)
		RETURNING id`

	return r.db.QueryRow(
		query,
		event.CreatedBy,
		event.CreatedAt,
		event.Title,
		event.Description,
		event.EventTime,
		event.RemindAt,
	).Scan(&event.ID)
}

func (r *PostgresRepository) Update(event *models.Event) error {
	query := `
		UPDATE events
		SET title = $1, description = $2, event_time = $3, remind_at = $4
		WHERE id = $5`

	result, err := r.db.Exec(
		query,
		event.Title,
		event.Description,
		event.EventTime,
		event.RemindAt,
		event.ID,
	)
	if err != nil {
		return err
	}

	rows, err := result.RowsAffected()
	if err != nil {
		return err
	}
	if rows == 0 {
		return sql.ErrNoRows
	}

	return nil
}

func (r *PostgresRepository) Delete(id int64) error {
	query := "DELETE FROM events WHERE id = $1"

	result, err := r.db.Exec(query, id)
	if err != nil {
		return err
	}

	rows, err := result.RowsAffected()
	if err != nil {
		return err
	}
	if rows == 0 {
		return sql.ErrNoRows
	}

	return nil
}

func (r *PostgresRepository) GetAll() ([]models.Event, error) {
	query := "SELECT id, created_by, created_at, title, description, event_time, remind_at FROM events"

	rows, err := r.db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var events []models.Event
	for rows.Next() {
		var event models.Event
		err := rows.Scan(
			&event.ID,
			&event.CreatedBy,
			&event.CreatedAt,
			&event.Title,
			&event.Description,
			&event.EventTime,
			&event.RemindAt,
		)
		if err != nil {
			return nil, err
		}
		events = append(events, event)
	}

	return events, nil
}

func (r *PostgresRepository) GetByID(id int64) (*models.Event, error) {
	query := "SELECT id, created_by, created_at, title, description, event_time, remind_at FROM events WHERE id = $1"

	event := &models.Event{}
	err := r.db.QueryRow(query, id).Scan(
		&event.ID,
		&event.CreatedBy,
		&event.CreatedAt,
		&event.Title,
		&event.Description,
		&event.EventTime,
		&event.RemindAt,
	)
	if err != nil {
		return nil, err
	}

	return event, nil
}
