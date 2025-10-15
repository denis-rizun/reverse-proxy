package main

import "reverse-proxy/src/internal/infrastructure/di"

func main() {
	bootstrap := di.NewBootstrap()
	bootstrap.Boot()
}
