package installer

import (
	"go.uber.org/zap"
	"os/exec"
	"strings"
)

type Executor struct {
	logger *zap.Logger
}

func NewExecutor(logger *zap.Logger) *Executor {
	return &Executor{
		logger: logger,
	}
}

func (e *Executor) Run(app string, args ...string) (string, error) {
	cmd := exec.Command(app, args...)
	e.logger.Debug("executing", zap.String("cmd", cmd.String()))
	out, err := cmd.CombinedOutput()
	e.logger.Debug("command output")
	for _, line := range strings.Split(string(out), "\n") {
		e.logger.Debug(line)
	}
	return string(out), err
}
