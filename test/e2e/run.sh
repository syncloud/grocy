#!/bin/bash -e

DIR=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "${DIR}/../.." && pwd)
cd "$DIR"

SPEC=$1

if [ -z "$SPEC" ]; then
  echo "usage: $0 spec"
  exit 1
fi

export PLAYWRIGHT_DOMAIN=buster.com
export PLAYWRIGHT_APP=grocy
export PLAYWRIGHT_DEVICE_USER=user
export PLAYWRIGHT_DEVICE_PASSWORD=Password1
export PLAYWRIGHT_PROJECT=desktop
export PLAYWRIGHT_ARTIFACT_DIR=${ROOT}/artifact/screenshots

mkdir -p ${PLAYWRIGHT_ARTIFACT_DIR}
trap 'chmod -R a+r ${PLAYWRIGHT_ARTIFACT_DIR}' EXIT

${ROOT}/apt.sh curl
npm ci --no-audit --no-fund
${DIR}/wait-app.sh ${PLAYWRIGHT_APP}.${PLAYWRIGHT_DOMAIN}
npx playwright test --project=${PLAYWRIGHT_PROJECT} "$SPEC"
