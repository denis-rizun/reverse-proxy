package network

import (
	"bytes"
	"errors"
	"strings"
)

type Request struct {
	Method  string
	Path    string
	Version string
	Headers map[string]string
}

func (s *Stream) ReadRequest() (*Request, error) {
	line, err := s.ReadLine()
	if err != nil {
		return nil, err
	}
	line = bytes.TrimSpace(line)
	if len(line) == 0 {
		return &Request{Method: "", Path: "", Version: "", Headers: nil}, nil
	}
	parts := strings.SplitN(string(line), " ", 3)
	if len(parts) != 3 {
		return nil, errors.New("invalid request line")
	}
	headers := make(map[string]string)
	for {
		l, err := s.ReadLine()
		if err != nil {
			return nil, err
		}
		tl := strings.TrimSpace(string(l))
		if tl == "" {
			break
		}
		kv := strings.SplitN(tl, ":", 2)
		if len(kv) != 2 {
			continue
		}
		headers[strings.ToLower(strings.TrimSpace(kv[0]))] = strings.TrimSpace(kv[1])
	}
	return &Request{
		Method:  parts[0],
		Path:    parts[1],
		Version: parts[2],
		Headers: headers,
	}, nil
}

func (r *Request) BuildLine() string {
	return r.Method + " " + r.Path + " " + r.Version
}
