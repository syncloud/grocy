#!/bin/bash -e
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )
${DIR}/bin/wait-for-configure.sh
exec $DIR/php/bin/php-fpm.sh -F -y ${SNAP_DATA}/config/php-fpm.conf -c ${SNAP_DATA}/config/php.ini
