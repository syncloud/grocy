package installer

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"go.uber.org/zap"
)

func TestExecutorRunReturnsOutput(t *testing.T) {
	executor := NewExecutor(zap.NewNop())
	out, err := executor.Run("echo", "grocy")
	assert.NoError(t, err)
	assert.Equal(t, "grocy\n", out)
}

func TestExecutorRunReturnsError(t *testing.T) {
	executor := NewExecutor(zap.NewNop())
	_, err := executor.Run("false")
	assert.Error(t, err)
}
