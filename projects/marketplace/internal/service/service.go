package service

import (
	"context"
	database "marketplace/internal/database"
	datamodel "marketplace/internal/datamodel"
)

type Service struct {
	accessor *database.AccessorDB
}

func (s *Service) AddProduct(ctx context.Context, product *datamodel.Product) error {
	return s.accessor.AddProduct(ctx, product)
}

func (s *Service) DumpAllProducts(ctx context.Context) ([]*datamodel.Product, error) {
	return s.accessor.DumpAllProducts(ctx)
}

func (s *Service) SearchProducts(ctx context.Context, name string) ([]*datamodel.Product, error) {
	return s.accessor.SearchProducts(ctx, name)
}

func NewService(accessor *database.AccessorDB) *Service {
	return &Service{accessor}
}
