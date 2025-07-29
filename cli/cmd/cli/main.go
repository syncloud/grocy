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
	var cmd = &cobra.Command{
		Use:          "cli",
		SilenceUsage: true,
	}

	cmd.AddCommand(&cobra.Command{
		Use: "storage-change",
		RunE: func(cmd *cobra.Command, args []string) error {
			logger := log.Logger(zap.DebugLevel)
			logger.Info("storage-change")
			install := installer.New(logger)
			return install.StorageChange()
		},
	})

	cmd.AddCommand(&cobra.Command{
		Use: "access-change",
		RunE: func(cmd *cobra.Command, args []string) error {
			logger := log.Logger(zap.DebugLevel)
			logger.Info("access-change")
			install := installer.New(logger)
			return install.AccessChange()
		},
	})

	cmd.AddCommand(&cobra.Command{
		Use: "backup-pre-stop",
		RunE: func(cmd *cobra.Command, args []string) error {
			logger := log.Logger(zap.DebugLevel)
			logger.Info("backup-pre-stop")
			install := installer.New(logger)
			return install.BackupPreStop()
		},
	})

	cmd.AddCommand(&cobra.Command{
		Use: "restore-pre-start",
		RunE: func(cmd *cobra.Command, args []string) error {
			logger := log.Logger(zap.DebugLevel)
			logger.Info("restore-pre-start")
			install := installer.New(logger)
			return install.RestorePreStart()
		},
	})

	cmd.AddCommand(&cobra.Command{
		Use: "restore-post-start",
		RunE: func(cmd *cobra.Command, args []string) error {
			logger := log.Logger(zap.DebugLevel)
			logger.Info("restore-post-start")
			install := installer.New(logger)
			return install.RestorePostStart()
		},
	})

	err := cmd.Execute()
	if err != nil {
		fmt.Print(err)
		os.Exit(1)
	}
}
