#!/bin/bash
set -e

if [ "$DB_MIGRATE" == "true" ]; then
    echo "Running database migration"
    flask db upgrade
else
    echo "Skipping database migration"
fi

exec gunicorn --worker-class=gevent --workers=3 -b 0.0.0.0:80 app:app --access-logfile access.log