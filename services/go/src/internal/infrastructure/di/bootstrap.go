package di

import (
	"reverse-proxy/src/internal/application"
	"reverse-proxy/src/internal/application/balancer"
	"reverse-proxy/src/internal/application/limiter"
	"reverse-proxy/src/internal/infrastructure/config"
	"strconv"
)

type Bootstrap struct{}

func NewBootstrap() *Bootstrap {
	return &Bootstrap{}
}

func (b *Bootstrap) Boot() {
	cfg, err := config.LoadConfig("config.yml")
	if err != nil {
		panic(err)
	}

	var upstreams []string
	for _, u := range cfg.Upstreams {
		upstreams = append(upstreams, u.GetString())
	}
	blc := balancer.NewBalancer(upstreams)
	lt := limiter.NewLimiter(50, 100)
	proxy := application.NewProxy(":"+strconv.Itoa(cfg.Listen.Port), blc, lt)
	server := application.NewServer(proxy)
	server.Start()
}
