CREATE DATABASE marketplace;
-- Мы используем существующего пользователя postgres
GRANT ALL PRIVILEGES ON DATABASE marketplace TO postgres;

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    sku VARCHAR(50) UNIQUE,
    price NUMERIC(10, 2)
);