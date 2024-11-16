package main

import (
	"fmt"
	"net/http"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

func initMetrics() prometheus.Counter {
	counter := prometheus.NewCounter(
		prometheus.CounterOpts{
			Name: "requests_count",
		},
	)
	prometheus.MustRegister(counter)

	return counter
}

func main() {
	metrics := initMetrics()

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("Hello world!"))
		metrics.Inc()
	})

	http.Handle("/metrics", promhttp.Handler())

	fmt.Println("Start server on :8082")
	http.ListenAndServe(":8082", nil)
}
