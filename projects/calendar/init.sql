CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    created_by VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    event_time TIMESTAMP NOT NULL,
    remind_at TIMESTAMP NOT NULL
);