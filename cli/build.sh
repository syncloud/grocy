#!/bin/bash -ex

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd ${DIR}

BUILD_DIR=${DIR}/../build/snap

CGO_ENABLED=0 go build -o ${BUILD_DIR}/meta/hooks/install ./cmd/install
CGO_ENABLED=0 go build -o ${BUILD_DIR}/meta/hooks/configure ./cmd/configure
CGO_ENABLED=0 go build -o ${BUILD_DIR}/meta/hooks/pre-refresh ./cmd/pre-refresh
CGO_ENABLED=0 go build -o ${BUILD_DIR}/meta/hooks/post-refresh ./cmd/post-refresh
CGO_ENABLED=0 go build -o ${BUILD_DIR}/bin/cli ./cmd/cli
