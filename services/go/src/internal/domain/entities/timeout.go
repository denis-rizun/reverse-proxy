package entities

import "time"

type Timeouts struct {
	ConnectMS int `yaml:"connect_ms"`
	ReadMS    int `yaml:"read_ms"`
	WriteMS   int `yaml:"write_ms"`
	TotalMS   int `yaml:"total_ms"`
}

func (t Timeouts) ToDuration() (connect, read, write, total time.Duration) {
	return time.Duration(t.ConnectMS) * time.Millisecond,
		time.Duration(t.ReadMS) * time.Millisecond,
		time.Duration(t.WriteMS) * time.Millisecond,
		time.Duration(t.TotalMS) * time.Millisecond
}
