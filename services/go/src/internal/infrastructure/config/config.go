package config

import (
	"errors"
	"gopkg.in/yaml.v3"
	"os"
	"reverse-proxy/src/internal/domain/entities"
)

type Config struct {
	Listen     entities.Address     `yaml:"listen"`
	Upstreams  []entities.Address   `yaml:"upstreams"`
	Timeouts   entities.Timeouts    `yaml:"timeouts"`
	Limits     entities.Limits      `yaml:"limits"`
	RateLimits entities.RateLimits  `yaml:"rate_limits"`
	Health     entities.HealthCheck `yaml:"health_check"`
}

func LoadConfig(path string) (*Config, error) {
	b, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	var cfg Config
	if err := yaml.Unmarshal(b, &cfg); err != nil {
		return nil, err
	}
	if len(cfg.Upstreams) == 0 {
		return nil, errors.New("missing upstreams")
	}
	return &cfg, nil
}
