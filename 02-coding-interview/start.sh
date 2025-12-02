#!/bin/sh
set -e

# Default to port 80 if not set
export PORT=${PORT:-80}

# Substitute PORT in nginx config
# We only substitute $PORT, keeping other nginx variables intact
envsubst '${PORT}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Start supervisor
exec /usr/bin/supervisord -c /etc/supervisord.conf
