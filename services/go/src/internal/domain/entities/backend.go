package entities

import "sync"

type Backend struct {
	Addr    string
	mu      sync.RWMutex
	Healthy bool
}

func (b *Backend) SetHealthy(v bool) {
	b.mu.Lock()
	b.Healthy = v
	b.mu.Unlock()
}

func (b *Backend) IsHealthy() bool {
	b.mu.RLock()
	defer b.mu.RUnlock()
	return b.Healthy
}
