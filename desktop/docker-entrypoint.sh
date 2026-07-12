#!/bin/sh
set -e

ADMIN_PASSWORD="${ADMIN_PASSWORD:-srp-admin}"

escaped_password=$(printf '%s' "$ADMIN_PASSWORD" | sed 's/\\/\\\\/g; s/"/\\"/g')
printf '{"adminPassword":"%s"}\n' "$escaped_password" > /usr/share/nginx/html/config.json

exec "$@"
