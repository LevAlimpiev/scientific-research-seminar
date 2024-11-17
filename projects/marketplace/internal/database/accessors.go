package database

import (
	"context"
	"database/sql"
	"marketplace/internal/datamodel"
)

type AccessorDB struct {
	db *sql.DB
}

func (a *AccessorDB) AddProduct(ctx context.Context, product *datamodel.Product) error {
	query := `INSERT INTO products (name, description, sku, price) VALUES ($1, $2, $3, $4)`
	_, err := a.db.ExecContext(ctx, query, product.Name, product.Description, product.SKU, product.Price)
	return err
}

func (a *AccessorDB) DumpAllProducts(ctx context.Context) ([]*datamodel.Product, error) {
	query := "SELECT id, name, description, sku, price FROM products"
	rows, err := a.db.QueryContext(ctx, query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var products []*datamodel.Product
	for rows.Next() {
		var product datamodel.Product
		if err := rows.Scan(&product.ID, &product.Name, &product.Description, &product.SKU, &product.Price); err != nil {
			return nil, err
		}
		products = append(products, &product)
	}

	return products, nil
}

func (a *AccessorDB) SearchProducts(ctx context.Context, name string) ([]*datamodel.Product, error) {
	query := `SELECT id, name, description, sku, price FROM products WHERE name ILIKE $1`
	rows, err := a.db.QueryContext(ctx, query, "%"+name+"%")
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var products []*datamodel.Product
	for rows.Next() {
		var product datamodel.Product
		if err := rows.Scan(&product.ID, &product.Name, &product.Description, &product.SKU, &product.Price); err != nil {
			return nil, err
		}
		products = append(products, &product)
	}

	return products, nil
}

func NewPostgresAccessor(db *sql.DB) *AccessorDB {
	return &AccessorDB{db: db}
}
