#!/bin/ash

set -e

if [ "$1" = 'burl' ]; then
    burl-manager migrate
    burl-manager collectstatic
    gunicorn -w 8 -b 0.0.0.0:8000 burl.core.wsgi:application
fi

exec "$@"