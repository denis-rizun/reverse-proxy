package limiter

import (
	"sync"
	"time"
)

type TokenBucket struct {
	rate     float64
	capacity float64
	tokens   float64
	last     time.Time
	mu       sync.Mutex
}

func NewTokenBucket(rate, capacity float64) *TokenBucket {
	return &TokenBucket{
		rate:     rate,
		capacity: capacity,
		tokens:   capacity,
		last:     time.Now(),
	}
}

func (b *TokenBucket) Consume(n float64) bool {
	b.mu.Lock()
	defer b.mu.Unlock()
	now := time.Now()
	elapsed := now.Sub(b.last).Seconds()
	b.last = now
	b.tokens += elapsed * b.rate
	if b.tokens > b.capacity {
		b.tokens = b.capacity
	}
	if b.tokens >= n {
		b.tokens -= n
		return true
	}
	return false
}
