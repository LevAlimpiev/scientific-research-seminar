package handlers

import (
	"encoding/json"
	"fmt"
	datamodel "marketplace/internal/datamodel"
	"marketplace/internal/service"
	"net/http"
)

type Handlers struct {
	service *service.Service
}

func (h *Handlers) AddProduct(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Handle Add Product")

	var product datamodel.Product
	if err := json.NewDecoder(r.Body).Decode(&product); err != nil {
		http.Error(w, "Failed parse input json", http.StatusBadRequest)
	}

	err := h.service.AddProduct(r.Context(), &product)

	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}

	w.WriteHeader(http.StatusOK)
}

func (h *Handlers) DumpAllProducts(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Handle Dump All Products")
	products, err := h.service.DumpAllProducts(r.Context())
	if err != nil {
		http.Error(w, "Failed to dump the database", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(products)
}

func (h *Handlers) SearchProducts(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Handle Search Products")
	query := r.URL.Query().Get("query")
	products, err := h.service.SearchProducts(r.Context(), query)
	if err != nil {
		http.Error(w, "Failed to dump the database", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(products)
}

func NewHandlers(service *service.Service) *Handlers {
	return &Handlers{service}
}
