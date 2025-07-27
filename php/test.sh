#!/bin/bash -ex

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd ${DIR}

BUILD_DIR=${DIR}/../build/snap/php
TEST_CONFIG_DIR=${DIR}/../build/config.test
cp -r ${DIR}/../config $TEST_CONFIG_DIR
sed -i "s#extension_dir.*#extension_dir=$BUILD_DIR/lib/php/extensions#g" $TEST_CONFIG_DIR/php.ini
sed -i "s#include=.*#include=$TEST_CONFIG_DIR/www.conf#g" $TEST_CONFIG_DIR/php-fpm.conf

${BUILD_DIR}/bin/php-fpm.sh -y $TEST_CONFIG_DIR/php-fpm.conf -c $TEST_CONFIG_DIR/php.ini --version
${BUILD_DIR}/bin/php-fpm.sh -y $TEST_CONFIG_DIR/php-fpm.conf -c $TEST_CONFIG_DIR/php.ini --version | ( ! grep Warning )
${BUILD_DIR}/bin/php.sh -c $TEST_CONFIG_DIR/php.ini --version
${BUILD_DIR}/bin/php.sh -c $TEST_CONFIG_DIR/php.ini -i
${BUILD_DIR}/bin/php.sh -c $TEST_CONFIG_DIR/php.ini -i | grep -i "gd support" | grep -i enabled
