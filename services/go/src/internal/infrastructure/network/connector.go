package network

import (
	"context"
	"net"
	"reverse-proxy/src/internal/application/balancer"
	"reverse-proxy/src/internal/infrastructure/config"
	"time"
)

type Connector struct {
	connectTimeout time.Duration
	lb             *balancer.LoadBalancer
}

func NewConnector(cfg *config.Config, lb *balancer.LoadBalancer) *Connector {
	connect, _, _, _ := cfg.Timeouts.ToDuration()
	return &Connector{
		connectTimeout: connect,
		lb:             lb,
	}
}

func (c *Connector) Connect(up balancer.Upstream) (*Stream, error) {
	ctx, cancel := context.WithTimeout(context.Background(), c.connectTimeout)
	defer cancel()
	d := &net.Dialer{}
	conn, err := d.DialContext(ctx, "tcp", up.Addr())
	if err != nil {
		c.lb.ReportFailure(up)
		return nil, err
	}
	return NewStream(conn), nil
}
