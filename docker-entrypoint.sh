#!/bin/bash

echo "Waiting for database..."
until nc -z db 5432; do
  sleep 1
done
echo "Database is up!"

echo "Applying migrations..."
python manage.py migrate

echo "Starting server..."
exec "$@"