#!/bin/bash -e

APP_DOMAIN=$1

getent ahosts "${APP_DOMAIN}" || true

OK=0
for i in $(seq 1 120); do
  RESULT=$(curl -skL -o /dev/null -w '%{http_code} %{remote_ip} %{url_effective}' "https://${APP_DOMAIN}" || true)
  echo "${APP_DOMAIN}: ${RESULT}"
  if [ "${RESULT%% *}" = "200" ]; then
    OK=$((OK + 1))
    if [ "$OK" -ge 3 ]; then
      exit 0
    fi
  else
    OK=0
  fi
  sleep 5
done

echo "${APP_DOMAIN} did not become ready"
exit 1
