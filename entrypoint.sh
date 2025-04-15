#!/bin/bash
PORT=8000

SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"admin@sociale.live"}
cd /app/

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true
gunicorn Sociale.wsgi:application --bind "0.0.0.0:${PORT}"
