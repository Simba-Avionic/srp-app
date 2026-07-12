#!/bin/sh
set -e

ADMIN_PASSWORD="${ADMIN_PASSWORD:-srp-admin}"
PROXY_UPSTREAM="${PROXY_UPSTREAM:-host.docker.internal:5000}"

escaped_password=$(printf '%s' "$ADMIN_PASSWORD" | sed 's/\\/\\\\/g; s/"/\\"/g')
printf '{"adminPassword":"%s"}\n' "$escaped_password" > /usr/share/nginx/html/config.json

export PROXY_UPSTREAM
envsubst '${PROXY_UPSTREAM}' \
  < /etc/nginx/templates/default.conf.template \
  > /etc/nginx/conf.d/default.conf

exec "$@"
