package entities

type HealthCheck struct {
	Interval int `yaml:"interval"`
	Timeout  int `yaml:"timeout"`
}
