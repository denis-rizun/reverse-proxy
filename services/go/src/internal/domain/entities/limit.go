package entities

type Limits struct {
	MaxClientConns      int `yaml:"max_client_conns"`
	MaxConnsPerUpstream int `yaml:"max_conns_per_upstream"`
}
