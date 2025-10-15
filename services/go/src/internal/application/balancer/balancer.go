package balancer

import (
	"fmt"
	"net"
	"sync"
	"time"

	"reverse-proxy/src/internal/domain/entities"
)

type Balancer struct {
	backends []*entities.Backend
	next     int
	mu       sync.Mutex
}

func NewBalancer(addrs []string) *Balancer {
	b := &Balancer{}
	for _, addr := range addrs {
		b.backends = append(b.backends, &entities.Backend{Addr: addr, Healthy: true})
	}
	go b.healthLoop()
	return b
}

func (b *Balancer) AcquireNext() (string, error) {
	b.mu.Lock()
	defer b.mu.Unlock()
	for i := 0; i < len(b.backends); i++ {
		be := b.backends[b.next]
		b.next = (b.next + 1) % len(b.backends)
		if be.IsHealthy() {
			return be.Addr, nil
		}
	}
	return "", fmt.Errorf("no healthy backend")
}

func (b *Balancer) Release(addr string) {}

func (b *Balancer) healthLoop() {
	ticker := time.NewTicker(5 * time.Second)
	defer ticker.Stop()

	sem := make(chan struct{}, 10)
	for range ticker.C {
		var wg sync.WaitGroup
		for _, be := range b.backends {
			wg.Add(1)
			sem <- struct{}{}
			go func(backend *entities.Backend) {
				defer func() { <-sem; wg.Done() }()
				conn, err := net.DialTimeout("tcp", backend.Addr, 500*time.Millisecond)
				if err != nil {
					backend.SetHealthy(false)
					return
				}
				conn.Close()
				backend.SetHealthy(true)
			}(be)
		}
		wg.Wait()
	}
}
