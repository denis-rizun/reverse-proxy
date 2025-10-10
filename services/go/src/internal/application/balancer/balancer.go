package balancer

import (
	"context"
	"errors"
	"fmt"
	"net"
	"reverse-proxy/src/internal/domain/enums"
	"reverse-proxy/src/internal/infrastructure/config"
	"reverse-proxy/src/internal/infrastructure/logger"
	"sync"
	"time"
)

type Upstream struct {
	Host   string
	Port   int
	Status enums.HealthStatus
}

func (u Upstream) Addr() string {
	return fmt.Sprintf("%s:%d", u.Host, u.Port)
}

type Semaphore chan struct{}

func NewSemaphore(max int) Semaphore {
	ch := make(Semaphore, max)
	for i := 0; i < max; i++ {
		ch <- struct{}{}
	}
	return ch
}

func (s Semaphore) Acquire(ctx context.Context) error {
	select {
	case <-ctx.Done():
		return ctx.Err()
	case <-s:
		return nil
	}
}

func (s Semaphore) Release() {
	select {
	default:
		s <- struct{}{}
	case <-time.After(time.Millisecond * 10):
		// shouldn't happen
	}
}

type LoadBalancer struct {
	Ups            []Upstream
	idx            int
	mu             sync.Mutex
	globalSem      Semaphore
	upstreamSems   map[string]Semaphore
	errorCounters  map[string]int
	circuitOpen    map[string]time.Time
	healthInterval time.Duration
	healthTimeout  time.Duration
	stopCh         chan struct{}
}

func NewLoadBalancer(cfg *config.Config) *LoadBalancer {
	ups := make([]Upstream, 0, len(cfg.Upstreams))
	for _, u := range cfg.Upstreams {
		ups = append(ups, Upstream{
			Host:   u.Host,
			Port:   u.Port,
			Status: enums.UP,
		})
	}
	lb := &LoadBalancer{
		Ups:            ups,
		idx:            0,
		globalSem:      NewSemaphore(cfg.Limits.MaxClientConns),
		upstreamSems:   make(map[string]Semaphore),
		errorCounters:  make(map[string]int),
		circuitOpen:    make(map[string]time.Time),
		healthInterval: time.Duration(cfg.Health.Interval) * time.Second,
		healthTimeout:  time.Duration(cfg.Health.Timeout) * time.Second,
		stopCh:         make(chan struct{}),
	}

	for _, u := range ups {
		lb.upstreamSems[u.Addr()] = NewSemaphore(cfg.Limits.MaxConnsPerUpstream)
		lb.errorCounters[u.Addr()] = 0
	}

	go lb.healthLoop()
	return lb
}

func (lb *LoadBalancer) AcquireNext(ctx context.Context) (Upstream, Semaphore, Semaphore, error) {
	lb.mu.Lock()
	defer lb.mu.Unlock()

	n := len(lb.Ups)
	for i := 0; i < n; i++ {
		lb.idx = (lb.idx + 1) % n
		up := lb.Ups[lb.idx]
		key := up.Addr()
		if up.Status == enums.DOWN {
			if until, ok := lb.circuitOpen[key]; ok && until.After(time.Now()) {
				continue
			}
		}
		us := lb.upstreamSems[key]
		return up, lb.globalSem, us, nil
	}
	return Upstream{}, nil, nil, errors.New("503 service unavailable")
}

func (lb *LoadBalancer) ReportFailure(up Upstream) {
	lb.mu.Lock()
	defer lb.mu.Unlock()
	key := up.Addr()
	lb.errorCounters[key]++
	if lb.errorCounters[key] >= 2 {
		for i := range lb.Ups {
			if lb.Ups[i].Addr() == key {
				lb.Ups[i].Status = enums.DOWN
			}
		}
		lb.circuitOpen[key] = time.Now().Add(10 * time.Second)
	}
}

func (lb *LoadBalancer) ReportSuccess(up Upstream) {
	lb.mu.Lock()
	defer lb.mu.Unlock()
	key := up.Addr()
	lb.errorCounters[key] = 0
	lb.circuitOpen[key] = time.Time{}
	for i := range lb.Ups {
		if lb.Ups[i].Addr() == key {
			lb.Ups[i].Status = enums.UP
		}
	}
}

func (lb *LoadBalancer) healthLoop() {
	t := time.NewTicker(lb.healthInterval)
	defer t.Stop()
	for {
		select {
		case <-t.C:
			for _, u := range lb.Ups {
				addr := u.Addr()
				ctx, cancel := context.WithTimeout(context.Background(), lb.healthTimeout)
				conn, err := (&net.Dialer{}).DialContext(ctx, "tcp", addr)
				cancel()
				if err == nil {
					err := conn.Close()
					if err != nil {
						return
					}
					lb.ReportSuccess(u)
				} else {
					logger.Info.Printf("healthcheck fail %s: %v", addr, err)
					lb.ReportFailure(u)
				}
			}
		case <-lb.stopCh:
			return
		}
	}
}
