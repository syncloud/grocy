#!/bin/bash -ex

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd ${DIR}

APCU=5.1.28
BUILD_DIR=${DIR}/../build/snap/php
mkdir -p ${BUILD_DIR}

${DIR}/../apt.sh --no-install-recommends \
  wget \
  libfreetype6-dev \
  libjpeg62-turbo-dev \
  libpng-dev \
  libwebp-dev \
  libzip-dev \
  libldap2-dev \
  libicu-dev \
  libonig-dev

${DIR}/../download-retry.sh https://pecl.php.net/get/apcu-${APCU}.tgz /tmp/apcu.tgz
pecl install /tmp/apcu.tgz
docker-php-ext-enable apcu

docker-php-ext-configure gd --with-freetype --with-jpeg --with-webp
docker-php-ext-install -j$(nproc) gd intl ldap zip bcmath exif

cp -r /usr ${BUILD_DIR}/
cp -r /lib ${BUILD_DIR}/
cp -r /bin ${BUILD_DIR}
cp ${DIR}/bin/* ${BUILD_DIR}/bin
mkdir -p ${BUILD_DIR}/lib/php/extensions
mv ${BUILD_DIR}/usr/local/lib/php/extensions/*/*.so ${BUILD_DIR}/lib/php/extensions
rm -rf ${BUILD_DIR}/usr/src
