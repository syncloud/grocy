#!/bin/sh -ex

DIR=$( cd "$( dirname "$0" )" && pwd )
cd ${DIR}

VERSION=$1
BUILD_DIR=${DIR}/build/snap
mkdir -p $BUILD_DIR

apt update
apt install -y wget bzip2 unzip


wget https://github.com/grocy/grocy/releases/download/v${VERSION}/grocy_${VERSION}.zip -O grocy.zip
unzip grocy.zip -d grocy
mv grocy ${BUILD_DIR}
