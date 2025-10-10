package network

import (
	"bufio"
	"io"
	"net"
	"strings"
)

type Stream struct {
	Conn   net.Conn
	Reader *bufio.Reader
	Writer *bufio.Writer
}

func NewStream(conn net.Conn) *Stream {
	return &Stream{
		Conn:   conn,
		Reader: bufio.NewReader(conn),
		Writer: bufio.NewWriter(conn),
	}
}

func (s *Stream) RemoteIP() string {
	if s.Conn == nil {
		return "unknown"
	}
	addr := s.Conn.RemoteAddr().String()
	if idx := strings.LastIndex(addr, ":"); idx != -1 {
		return addr[:idx]
	}
	return addr
}

func (s *Stream) Write(b []byte, flush bool) error {
	if _, err := s.Writer.Write(b); err != nil {
		return err
	}
	if flush {
		return s.Writer.Flush()
	}
	return nil
}

func (s *Stream) Read(n int) ([]byte, error) {
	buf := make([]byte, n)
	nn, err := s.Reader.Read(buf)
	return buf[:nn], err
}

func (s *Stream) ReadLine() ([]byte, error) {
	line, err := s.Reader.ReadBytes('\n')
	return line, err
}

func (s *Stream) ReadExactly(n int) ([]byte, error) {
	buf := make([]byte, n)
	_, err := io.ReadFull(s.Reader, buf)
	return buf, err
}

func (s *Stream) Close() error {
	return s.Conn.Close()
}
