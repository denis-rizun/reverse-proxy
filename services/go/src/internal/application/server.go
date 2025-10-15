package application

import (
	"net"
	"reverse-proxy/src/internal/infrastructure/logger"
)

type Server struct {
	proxy *Proxy
}

func NewServer(proxy *Proxy) *Server {
	return &Server{proxy: proxy}
}

func (ser *Server) Start() {
	listener, err := net.Listen("tcp", ser.proxy.addr)
	if err != nil {
		logger.Error.Fatal(err)
	}
	defer listener.Close()

	logger.Info.Printf("Proxy listening on %s", ser.proxy.addr)
	for {
		conn, err := listener.Accept()
		if err != nil {
			continue
		}
		go ser.proxy.Handle(conn)
	}
}
