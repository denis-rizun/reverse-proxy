package network

import "strings"

type Request struct {
	Method string
	Host   string
	Path   string
}

func (*Request) ReadRequest(reader []byte) (*Request, error) {
	raw := string(reader)
	lines := strings.SplitN(raw, "\r\n", 2)
	reqLine := lines[0]

	parts := strings.Split(reqLine, " ")
	method, path := "-", "-"
	if len(parts) >= 2 {
		method = parts[0]
		path = parts[1]
	}

	host := "-"
	for _, line := range strings.Split(raw, "\r\n") {
		if strings.HasPrefix(strings.ToLower(line), "host:") {
			host = strings.TrimSpace(strings.TrimPrefix(line, "host:"))
			break
		}
	}

	return &Request{
		Method: method,
		Host:   host,
		Path:   path,
	}, nil
}
