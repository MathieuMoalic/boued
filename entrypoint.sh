#!/bin/sh
set -e

DATABASE_PATH=${DATABASE_URL#sqlite:///}

if [ -f $DATABASE_PATH ]; then
    cd /app/backend/migrations
    alembic upgrade head
else
    echo "Database not found, creating a new one"
fi 

cd /app
exec uvicorn backend.main:app --proxy-headers --host 0.0.0.0 --port 6001
