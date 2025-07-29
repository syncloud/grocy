package main

import (
	"fmt"
	"github.com/spf13/cobra"
	"go.uber.org/zap"
	"hooks/installer"
	"hooks/log"
	"os"
)

func main() {
	var rootCmd = &cobra.Command{
		SilenceUsage: true,
		RunE: func(cmd *cobra.Command, args []string) error {
			logger := log.Logger(zap.DebugLevel)
			return installer.New(logger).PostRefresh()
		},
	}

	err := rootCmd.Execute()
	if err != nil {
		fmt.Print(err)
		os.Exit(1)
	}
}
