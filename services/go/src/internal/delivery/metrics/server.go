package metrics

import (
	"fmt"
	"net/http"
	"sync/atomic"
)

var (
	totalRequests  uint64
	activeConns    int64
	failedRequests uint64
)

func IncRequests() { atomic.AddUint64(&totalRequests, 1) }
func IncActive()   { atomic.AddInt64(&activeConns, 1) }
func DecActive()   { atomic.AddInt64(&activeConns, -1) }
func IncFailed()   { atomic.AddUint64(&failedRequests, 1) }

func GetTotal() uint64  { return atomic.LoadUint64(&totalRequests) }
func GetActive() int64  { return atomic.LoadInt64(&activeConns) }
func GetFailed() uint64 { return atomic.LoadUint64(&failedRequests) }

func StartMetricsServer(addr string) {
	http.HandleFunc("/metrics", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		fmt.Fprintf(w, `
		<html>
		<head><title>Proxy Metrics</title></head>
		<body>
			<h1>Reverse Proxy Metrics</h1>
			<ul>
				<li>Total Requests: %d</li>
				<li>Active Connections: %d</li>
				<li>Failed Requests: %d</li>
			</ul>
		</body>
		</html>
		`, GetTotal(), GetActive(), GetFailed())
	})
	go func() {
		if err := http.ListenAndServe(addr, nil); err != nil {
			panic(err)
		}
	}()
}
