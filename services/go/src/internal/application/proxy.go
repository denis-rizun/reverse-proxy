package application

import (
	"context"
	"errors"
	"io"
	"reverse-proxy/src/internal/delivery/metrics"
	"time"

	"reverse-proxy/src/internal/application/balancer"
	"reverse-proxy/src/internal/application/limiter"
	"reverse-proxy/src/internal/infrastructure/config"
	"reverse-proxy/src/internal/infrastructure/logger"
	"reverse-proxy/src/internal/infrastructure/network"
)

type Proxy struct {
	cfg       *config.Config
	lb        *balancer.LoadBalancer
	limiter   *limiter.RateLimiter
	connector *network.Connector
}

func NewProxy(
	cfg *config.Config,
	lb *balancer.LoadBalancer,
	limiter *limiter.RateLimiter,
	connector *network.Connector,
) *Proxy {
	return &Proxy{cfg: cfg, lb: lb, limiter: limiter, connector: connector}
}

func (p *Proxy) Handle(client *network.Stream) error {
	metrics.IncActive()
	defer metrics.DecActive()
	defer client.Close()

	for {
		clientIP := client.RemoteIP()

		if !p.limiter.Allow(clientIP) {
			metrics.IncFailed()
			_ = client.Write([]byte("HTTP/1.1 429 Too Many Requests\r\nConnection: close\r\n\r\n"), true)
			return nil
		}

		startRead := time.Now()
		req, err := client.ReadRequest()
		readDuration := time.Since(startRead)
		if err != nil {
			if err == io.EOF {
				return nil
			}
			metrics.IncFailed()
			return err
		}
		if req.Method == "" {
			return nil
		}

		metrics.IncRequests()

		var lastErr error
		attempts := len(p.lb.Ups)
		success := false

		for i := 0; i < attempts; i++ {
			up, gSem, upSem, err := p.lb.AcquireNext(context.Background())
			if err != nil {
				metrics.IncFailed()
				return err
			}

			ctx, cancel := context.WithTimeout(context.Background(), 100*time.Millisecond)
			if err := gSem.Acquire(ctx); err != nil {
				cancel()
				continue
			}
			if err := upSem.Acquire(ctx); err != nil {
				gSem.Release()
				cancel()
				continue
			}
			cancel()

			startForward := time.Now()
			upstreamStream, err := p.connector.Connect(up)
			if err != nil {
				p.lb.ReportFailure(up)
				upSem.Release()
				gSem.Release()
				lastErr = err
				metrics.IncFailed()
				continue
			}

			if err := network.Forward(req, client, upstreamStream, clientIP); err != nil {
				p.lb.ReportFailure(up)
				_ = upstreamStream.Close()
				upSem.Release()
				gSem.Release()
				lastErr = err
				metrics.IncFailed()
				continue
			}
			forwardDuration := time.Since(startForward)

			startTTFB := time.Now()
			firstChunk, _ := upstreamStream.Read(1)
			ttfbDuration := time.Since(startTTFB)

			go func() {
				defer upstreamStream.Close()
				defer upSem.Release()
				defer gSem.Release()
				if len(firstChunk) > 0 {
					_ = client.Write(firstChunk, false)
				}
				buf := make([]byte, 8192)
				for {
					n, err := upstreamStream.Reader.Read(buf)
					if n > 0 {
						if err := client.Write(buf[:n], true); err != nil {
							return
						}
					}
					if err != nil {
						break
					}
				}
			}()

			logger.Info.Printf(
				"%s | %s:%d | R: %.1fms F: %.1fms TTFB: %.1fms",
				req.Method+" "+req.Path,
				up.Host, up.Port,
				float64(readDuration.Microseconds())/1000,
				float64(forwardDuration.Microseconds())/1000,
				float64(ttfbDuration.Microseconds())/1000,
			)

			success = true
			break
		}

		if !success {
			if lastErr != nil {
				logger.Info.Printf("request failed: %v", lastErr)
				metrics.IncFailed()
				return lastErr
			}
			metrics.IncFailed()
			return errors.New("503 service unavailable")
		}
	}
}
