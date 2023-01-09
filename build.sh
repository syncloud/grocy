#!/bin/bash -ex

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd ${DIR}

BUILD_DIR=${DIR}/build/snap

# Copy default config
cp grocy/config-dist.php config/config.php

# From Nextcloud's build.sh; seems redundant to me because these directories are also copied in package.sh
# cp -r bin ${BUILD_DIR}
# cp -r config ${BUILD_DIR}
# cp -r hooks ${BUILD_DIR}
