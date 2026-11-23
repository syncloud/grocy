#!/bin/bash -ex

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd ${DIR}

BUILD_DIR=${DIR}/../build/snap/php
TEST_CONFIG_DIR=$(mktemp -d)
cp -r ${DIR}/../config/. ${TEST_CONFIG_DIR}
sed -i "s#extension_dir.*#extension_dir=${BUILD_DIR}/lib/php/extensions#g" ${TEST_CONFIG_DIR}/php.ini

${BUILD_DIR}/bin/php-fpm.sh -y ${TEST_CONFIG_DIR}/php-fpm.conf -c ${TEST_CONFIG_DIR}/php.ini --version
${BUILD_DIR}/bin/php-fpm.sh -y ${TEST_CONFIG_DIR}/php-fpm.conf -c ${TEST_CONFIG_DIR}/php.ini --version 2>&1 | ( ! grep -i warning )
${BUILD_DIR}/bin/php.sh -c ${TEST_CONFIG_DIR}/php.ini --version 2>&1 | ( ! grep -i warning )
MODULES=$(${BUILD_DIR}/bin/php.sh -c ${TEST_CONFIG_DIR}/php.ini -m)
for module in fileinfo pdo_sqlite gd ctype intl zlib mbstring filter iconv tokenizer json ldap apcu zip "Zend OPcache"; do
  echo "${MODULES}" | grep -qx "${module}"
done
${BUILD_DIR}/bin/php.sh -c ${TEST_CONFIG_DIR}/php.ini -i | grep -i "gd support" | grep -i enabled
${BUILD_DIR}/bin/php.sh -c ${TEST_CONFIG_DIR}/php.ini -r 'exit(version_compare(SQLite3::version()["versionString"], "3.40.0", ">=") ? 0 : 1);'
rm -rf ${TEST_CONFIG_DIR}
