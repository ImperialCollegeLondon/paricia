#!/bin/sh

echo "Running migrations..."
python manage.py migrate

echo "Starting Huey task queue..."
python manage.py run_huey &

echo "Starting Gunicorn:..."
exec gunicorn djangomain.wsgi:application --bind 0.0.0.0:8000
