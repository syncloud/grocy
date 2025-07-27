#!/bin/sh -xe

DIR=$( cd "$( dirname "$0" )" && pwd )
cd ${DIR}

BUILD_DIR=${DIR}/../build/snap/php

mkdir -p ${BUILD_DIR}
cd ${BUILD_DIR}

apt-get update
apt-get install -y \
		libfreetype6-dev \
		libjpeg62-turbo-dev \
		libpng-dev \
		libzip-dev \
		libsmbclient-dev \
		libxml2-dev \
		libsqlite3-dev \
		libpq-dev \
		libldap2-dev \
		libsasl2-dev \
		libfreetype6-dev \
		liblqr-1-0-dev \
		libfftw3-dev \
		libjbig-dev \
		libtiff5-dev \
		libwebp-dev \
		libmemcached-dev \
    libmcrypt-dev \
		zip \
		wget \
		unzip \
    libgmp-dev \
    libonig-dev \
    libicu-dev \
    libmagickwand-dev \
    libbz2-dev \
    git \
    --no-install-recommends

mkdir -p /usr/src/php/ext/memcached
cd /usr/src/php/ext/memcached
wget https://github.com/php-memcached-dev/php-memcached/archive/v3.1.5.zip
unzip /usr/src/php/ext/memcached/v*.zip
mv /usr/src/php/ext/memcached/php-memcached-*/* /usr/src/php/ext/memcached/

docker-php-ext-install bz2
docker-php-ext-configure memcached
docker-php-ext-install memcached
docker-php-ext-install gmp
#RUN pecl install imagick
git clone https://github.com/Imagick/imagick.git --depth 1 /tmp/imagick && \
    cd /tmp/imagick && \
    git fetch origin master && \
    git switch master && \
    cd /tmp/imagick && \
    phpize && \
    ./configure && \
    make && \
    make install && \
    docker-php-ext-enable imagick

pecl install smbclient
pecl install apcu
pecl install mcrypt-1.0.7
pecl install redis
docker-php-ext-enable redis
docker-php-ext-configure intl
docker-php-ext-install intl
docker-php-ext-enable apcu
docker-php-ext-install ldap
docker-php-ext-enable mcrypt
docker-php-ext-install bcmath
docker-php-ext-install pdo_mysql
docker-php-ext-install mysqli
docker-php-ext-install mbstring
docker-php-ext-install opcache
docker-php-ext-install zip
docker-php-ext-install pcntl
docker-php-ext-install exif
docker-php-ext-install sysvsem
#RUN docker-php-ext-enable imagick

docker-php-ext-enable smbclient
docker-php-ext-install pdo pdo_pgsql
docker-php-ext-configure gd --with-freetype --with-jpeg
docker-php-ext-install -j2 gd

apt remove -y git

cp -r /usr ${BUILD_DIR}/
cp -r /lib ${BUILD_DIR}/
cp -r /bin ${BUILD_DIR}

mv ${BUILD_DIR}/usr/lib/*-linux*/ImageMagick-*/modules-*/coders ${BUILD_DIR}/usr/lib/ImageMagickCoders
ls -la ${BUILD_DIR}/usr/lib/ImageMagickCoders
cp ${DIR}/bin/* ${BUILD_DIR}/bin
mkdir -p ${BUILD_DIR}/lib/php/extensions
mv ${BUILD_DIR}/usr/local/lib/php/extensions/*/*.so ${BUILD_DIR}/lib/php/extensions
rm -rf ${BUILD_DIR}/usr/src
