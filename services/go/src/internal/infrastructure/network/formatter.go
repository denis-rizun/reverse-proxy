package network

import "strings"

var hopByHop = map[string]struct{}{
	"connection":          {},
	"keep-alive":          {},
	"proxy-authenticate":  {},
	"proxy-authorization": {},
	"te":                  {},
	"trailers":            {},
	"transfer-encoding":   {},
	"upgrade":             {},
	"proxy-connection":    {},
}

func FormatHeaders(r *Request, clientIP string) map[string]string {
	headers := make(map[string]string)
	for k, v := range r.Headers {
		headers[k] = v
	}
	if clientIP != "" {
		if v, ok := headers["x-forwarded-for"]; ok && v != "" {
			headers["x-forwarded-for"] = v + ", " + clientIP
		} else {
			headers["x-forwarded-for"] = clientIP
		}
	}
	via := "1.1 my-proxy"
	if v, ok := headers["via"]; ok && v != "" {
		headers["via"] = v + ", " + via
	} else {
		headers["via"] = via
	}
	headers["connection"] = "keep-alive"

	for k := range headers {
		if _, ok := hopByHop[strings.ToLower(k)]; ok {
			delete(headers, k)
		}
	}
	return headers
}
