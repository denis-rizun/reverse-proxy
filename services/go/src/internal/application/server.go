package application

import (
	"net"
	"reverse-proxy/src/internal/infrastructure/logger"
	"reverse-proxy/src/internal/infrastructure/network"
)

type Server struct {
	proxy *Proxy
}

func NewServer(proxy *Proxy) *Server {
	return &Server{proxy: proxy}
}

func (ser *Server) Serve(listener net.Listener) {
	for {
		conn, err := listener.Accept()
		if err != nil {
			logger.Info.Printf("accept: %v", err)
			continue
		}
		s := network.NewStream(conn)

		go func() {
			if err := ser.proxy.Handle(s); err != nil {
				logger.Error.Printf("proxy handle: %v", err)
			}
		}()
	}
}
