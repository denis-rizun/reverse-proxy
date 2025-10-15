package limiter

import (
	"sync"
	"time"
)

type TokenBucket struct {
	mu       sync.RWMutex
	tokens   float64
	last     time.Time
	rate     float64
	capacity float64
}

func NewTokenBucket(rate, capacity float64) *TokenBucket {
	return &TokenBucket{
		tokens:   capacity,
		last:     time.Now(),
		rate:     rate,
		capacity: capacity,
	}
}

func (b *TokenBucket) Allow() bool {
	b.mu.Lock()
	defer b.mu.Unlock()

	elapsed := time.Since(b.last).Seconds()
	b.tokens += elapsed * b.rate
	if b.tokens > b.capacity {
		b.tokens = b.capacity
	}
	b.last = time.Now()

	if b.tokens < 1 {
		return false
	}

	b.tokens -= 1
	return true
}
