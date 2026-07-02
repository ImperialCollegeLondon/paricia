#!/bin/sh

echo "Running migrations..."
python manage.py migrate

echo "Starting Django server..."
python manage.py run_huey &
python manage.py runserver 0:8000
