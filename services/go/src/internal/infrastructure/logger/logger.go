package logger

import (
	"log"
	"os"
	"reverse-proxy/src/internal/core"
)

var (
	Info  *log.Logger
	Error *log.Logger
)

func init() {
	Info = log.New(
		os.Stdout,
		core.GreenColor+"INFO: "+core.ResetColor, log.Ldate|log.Ltime|log.Lmsgprefix,
	)
	Error = log.New(
		os.Stderr,
		core.RedColor+"ERROR: "+core.ResetColor, log.Ldate|log.Ltime|log.Lmsgprefix,
	)
}
