#!/bin/sh -ex

DIR=$( cd "$( dirname "$0" )" && pwd )
cd ${DIR}

ARCH=$(uname -m)
DOWNLOAD_URL=https://github.com/syncloud/3rdparty/releases/download/
VERSION=$1
apt update
apt install -y wget bzip2 unzip

BUILD_DIR=${DIR}/build/snap
mkdir -p $BUILD_DIR

cd ${DIR}/build
wget ${DOWNLOAD_URL}/nginx/nginx-${ARCH}.tar.gz
tar xf nginx-${ARCH}.tar.gz
mv nginx ${BUILD_DIR}

wget https://github.com/grocy/grocy/releases/download/v${VERSION}/grocy_${VERSION}.zip -O grocy.zip
unzip grocy.zip -d grocy
mv grocy ${BUILD_DIR}
