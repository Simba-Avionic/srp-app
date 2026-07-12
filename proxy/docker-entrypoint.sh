#!/bin/sh
set -e

if [ -n "${MULTICAST_GROUP:-}" ]; then
    ip addr show dev lo 2>/dev/null | grep -q "${MULTICAST_GROUP}" || \
        ip addr add "${MULTICAST_GROUP}" dev lo autojoin 2>/dev/null || true
fi

exec "$@"
