package limiter

import "sync"

type RateLimiter struct {
	perUpstream bool
	global      *TokenBucket
	clients     map[string]*TokenBucket
	mu          sync.Mutex
	rate        float64
	capacity    float64
}

func NewRateLimiter(rate, capacity float64, perUpstream bool) *RateLimiter {
	return &RateLimiter{
		perUpstream: perUpstream,
		global:      NewTokenBucket(rate, capacity),
		clients:     make(map[string]*TokenBucket),
		rate:        rate,
		capacity:    capacity,
	}
}

func (r *RateLimiter) Allow(clientIP string) bool {
	if r.perUpstream && clientIP != "" {
		r.mu.Lock()
		b, ok := r.clients[clientIP]
		if !ok {
			b = NewTokenBucket(r.rate, r.capacity)
			r.clients[clientIP] = b
		}
		r.mu.Unlock()
		return b.Consume(1)
	}
	return r.global.Consume(1)
}
