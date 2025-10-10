package entities

type RateLimits struct {
	Rate        float64 `yaml:"rate"`
	Capacity    float64 `yaml:"capacity"`
	PerUpstream bool    `yaml:"per_upstream"`
}
