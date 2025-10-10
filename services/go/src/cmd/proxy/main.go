package main

import (
	"flag"
	"fmt"
	"net"
	"os"
	"reverse-proxy/src/internal/application"
	"reverse-proxy/src/internal/application/balancer"
	"reverse-proxy/src/internal/application/limiter"
	"reverse-proxy/src/internal/delivery/metrics"
	"reverse-proxy/src/internal/infrastructure/config"
	"reverse-proxy/src/internal/infrastructure/logger"
	"reverse-proxy/src/internal/infrastructure/network"
)

func main() {
	cfgPath := flag.String("c", "config.yml", "config path")
	flag.Parse()

	cfg, err := config.LoadConfig(*cfgPath)
	if err != nil {
		logger.Error.Printf("config load: %v", err)
	}
	lb := balancer.NewLoadBalancer(cfg)
	lim := limiter.NewRateLimiter(cfg.RateLimits.Rate, cfg.RateLimits.Capacity, cfg.RateLimits.PerUpstream)
	connector := network.NewConnector(cfg, lb)
	proxy := application.NewProxy(cfg, lb, lim, connector)
	server := application.NewServer(proxy)

	addr := fmt.Sprintf("%s:%d", cfg.Listen.Host, cfg.Listen.Port)
	ln, err := net.Listen("tcp", addr)
	if err != nil {
		logger.Info.Printf("listen: %v", err)
		os.Exit(1)
	}
	logger.Info.Printf("listening %s", addr)

	metrics.StartMetricsServer(":9090")
	server.Serve(ln)
}
