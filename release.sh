#!/usr/bin/env bash
set -euo pipefail

echo "Starting release script..."

# Activate venv if created by the build process
if [ -f /app/.venv/bin/activate ]; then
  . /app/.venv/bin/activate
fi

# Ensure STATIC_ROOT exists (safety for WhiteNoise)
# Don't import Django settings here because DJANGO_SETTINGS_MODULE may not be set
# in the build/release environment. Create the conventional staticfiles path.
mkdir -p /app/staticfiles || true
echo "Ensured STATIC_ROOT: /app/staticfiles"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Release script completed."
