#!/usr/bin/env bash
# Exit in error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Coolect static files
python manage.py collectstatic --no-input

# Apply migrations
python manage.py migrate

# Create superuser if not already exists
if [[ -z "${DJANGO_SUPERUSER_USERNAME}" || -z "${DJANGO_SUPERUSER_EMAIL}" || -z "${DJANGO_SUPERUSER_PASSWORD}" ]]; then
  echo "Environment variables for superuser are not set. Skipping superuser creation."
else
  python manage.py createsuperuser --noinput || echo "Superuser already exists."
fi