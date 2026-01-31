#!/usr/bin/env bash
set -e

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
gunicorn senescence.wsgi:application --bind 0.0.0.0:${PORT:-8000}
