package network

import (
	"fmt"
	"strconv"
)

func Forward(req *Request, client *Stream, upstream *Stream, clientIP string) error {
	headers := FormatHeaders(req, clientIP)
	if err := upstream.Write([]byte(req.BuildLine()+"\r\n"), false); err != nil {
		return err
	}
	for k, v := range headers {
		if err := upstream.Write([]byte(fmt.Sprintf("%s: %s\r\n", k, v)), false); err != nil {
			return err
		}
	}
	if err := upstream.Write([]byte("\r\n"), true); err != nil {
		return err
	}

	if cl, ok := headers["content-length"]; ok {
		n, _ := strconv.Atoi(cl)
		remaining := n
		bufSize := 8192
		for remaining > 0 {
			toRead := bufSize
			if remaining < bufSize {
				toRead = remaining
			}
			chunk, err := client.Read(toRead)
			if err != nil {
				return err
			}
			if len(chunk) == 0 {
				break
			}
			if err := upstream.Write(chunk, true); err != nil {
				return err
			}
			remaining -= len(chunk)
		}
	} else if te, ok := headers["transfer-encoding"]; ok && te == "chunked" {
		for {
			line, err := client.ReadLine()
			if err != nil {
				return err
			}
			if err := upstream.Write(line, true); err != nil {
				return err
			}
			// parse chunk size
			sizeLine := string(line)
			size, _ := strconv.ParseInt(sizeLine, 16, 64)
			if size == 0 {
				rest, _ := client.ReadLine()
				upstream.Write(rest, true)
				break
			}
			chunk, err := client.ReadExactly(int(size) + 2) // +CRLF
			if err != nil {
				return err
			}
			if err := upstream.Write(chunk, true); err != nil {
				return err
			}
		}
	}
	return nil
}
