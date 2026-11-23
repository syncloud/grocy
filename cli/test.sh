#!/bin/bash -ex

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

BUILD_DIR=${DIR}/../build/snap

${BUILD_DIR}/bin/cli --help
${BUILD_DIR}/meta/hooks/install --help
${BUILD_DIR}/meta/hooks/configure --help
${BUILD_DIR}/meta/hooks/pre-refresh --help
${BUILD_DIR}/meta/hooks/post-refresh --help
