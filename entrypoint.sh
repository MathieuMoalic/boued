#!/bin/sh
set -e

if [ "$(echo $DATABASE_URL | cut -c1-9)" != "sqlite://" ]; then
    echo "Database URL is not valid"
    exit 1
fi

DATABASE_PATH=${DATABASE_URL#sqlite:///}

if [ -f $DATABASE_PATH ]; then
    cd /app/backend/migrations
    VERSION=$(sqlite3 "$DATABASE_PATH" "SELECT version FROM version;" 2>/dev/null)
    echo "Current version: $VERSION"

    # get the last migration version from the .sql files
    LAST_MIGRATION=$(ls -1 *.sql | sort -n | tail -n 1 | sed 's/\.sql//')
    echo "Last migration: $LAST_MIGRATION"
    
    # apply all needed migrations
    for i in $(seq $VERSION $LAST_MIGRATION); do
        echo "Applying migration $i"
        sqlite3 $DATABASE_PATH < $i.sql
    done
else
    echo "Database not found, creating a new one"
fi 

cd /app
exec uvicorn backend.main:app --proxy-headers --host 0.0.0.0 --port 6001
