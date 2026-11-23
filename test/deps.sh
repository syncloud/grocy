#!/bin/bash -e

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

${DIR}/../apt.sh sshpass openssh-client
pip install --retries 10 -r ${DIR}/requirements.txt
