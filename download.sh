#!/bin/bash -ex

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd ${DIR}

VERSION=$1
BUILD_DIR=${DIR}/build/snap
mkdir -p ${BUILD_DIR}

${DIR}/apt.sh wget unzip
${DIR}/download-retry.sh https://github.com/grocy/grocy/releases/download/v${VERSION}/grocy_${VERSION}.zip ${DIR}/build/grocy.zip
rm -rf ${BUILD_DIR}/grocy
unzip -q ${DIR}/build/grocy.zip -d ${BUILD_DIR}/grocy
