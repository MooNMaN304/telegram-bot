#!/bin/bash
set -e

echo "================================"
echo "Starting Telegram Bot..."
echo "================================"

echo ""
echo "[1/2] Waiting for PostgreSQL to be ready..."
max_attempts=30
attempt=1
while ! nc -z postgres 5432; do
    if [ $attempt -ge $max_attempts ]; then
        echo "PostgreSQL did not become available in time"
        exit 1
    fi
    echo "  Attempt $attempt/$max_attempts - PostgreSQL is unavailable, sleeping..."
    sleep 1
    attempt=$((attempt + 1))
done
echo "✓ PostgreSQL is ready!"

echo ""
echo "[2/2] Running Alembic migrations..."
if alembic upgrade head; then
    echo "✓ Migrations completed successfully!"
else
    echo "✗ Migrations failed!"
    exit 1
fi

echo ""
echo "================================"
echo "Starting bot application..."
echo "================================"
exec python -m src.main
