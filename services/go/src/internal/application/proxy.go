package application

import (
	"errors"
	"io"
	"net"
	"time"

	bl "reverse-proxy/src/internal/application/balancer"
	lm "reverse-proxy/src/internal/application/limiter"
	"reverse-proxy/src/internal/infrastructure/logger"
	nw "reverse-proxy/src/internal/infrastructure/network"
)

type Proxy struct {
	addr     string
	balancer *bl.Balancer
	limiter  *lm.RateLimiter
	parser   *nw.Request
}

func NewProxy(addr string, b *bl.Balancer, l *lm.RateLimiter) *Proxy {
	return &Proxy{addr: addr, balancer: b, limiter: l}
}

func (p *Proxy) Handle(client net.Conn) {
	if !p.limiter.Allow(client.RemoteAddr().String()) {
		client.Close()
		return
	}

	upstream, err := p.balancer.AcquireNext()
	if err != nil {
		client.Close()
		return
	}
	defer p.balancer.Release(upstream)

	server, err := net.DialTimeout("tcp", upstream, 3*time.Second)
	if err != nil {
		client.Close()
		return
	}
	defer client.Close()
	defer server.Close()

	go io.Copy(server, client)
	go io.Copy(client, server)

	reader := make([]byte, 4096)
	for {
		client.SetReadDeadline(time.Now().Add(5 * time.Second))
		n, err := client.Read(reader)
		if err != nil {
			var ne net.Error
			if errors.As(err, &ne) && ne.Timeout() {
				continue
			}
			return
		}

		req, _ := p.parser.ReadRequest(reader)
		logger.Info.Printf("%s %s | %s -> %s", req.Method, req.Path, req.Host, upstream)

		server.Write(reader[:n])
	}
}
