package limiter

import "sync"

type RateLimiter struct {
	buckets  sync.Map
	rate     float64
	capacity float64
}

func NewLimiter(rate, capacity float64) *RateLimiter {
	return &RateLimiter{rate: rate, capacity: capacity}
}

func (l *RateLimiter) Allow(key string) bool {
	val, ok := l.buckets.Load(key)
	if ok {
		return val.(*TokenBucket).Allow()
	}
	tb := NewTokenBucket(l.rate, l.capacity)
	l.buckets.Store(key, tb)
	return tb.Allow()
}
