package entities

type Address struct {
	Host string `yaml:"host"`
	Port int    `yaml:"port"`
}

func (a Address) GetString() string {
	return a.Host + ":" + string(rune(a.Port))
}
