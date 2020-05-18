#!/bin/ash

set -e

if [ "$1" = 'run' ]; then
    if [ -n "$2" ]; then
        workers=$2
    else
        workers=8
    fi
    if [ -n "$3" ]; then
        bind=$3
    else
        bind=0.0.0.0:8000
    fi
    burl-manager migrate --no-input
    burl-manager collectstatic --no-input
    gunicorn -w $workers -b $bind burl.core.wsgi:application
elif [ "$1" = 'manage' ]; then
    args=$(echo ${*} | cut -d " " -f 2-)
    burl-manager $args
fi
