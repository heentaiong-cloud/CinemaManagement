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
# Ensure MEDIA_ROOT exists so FileField uploads won't fail when saving files
mkdir -p /app/media || true
echo "Ensured MEDIA_ROOT: /app/media"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Generating favicon if missing..."
if [ -f scripts/generate_favicon.py ]; then
  python scripts/generate_favicon.py || echo "favicon generation failed (continuing)"
else
  echo "generate_favicon.py not found, skipping"
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Running optional admin creation from environment..."
if [ -f scripts/create_admin.py ]; then
  python scripts/create_admin.py || echo "create_admin.py returned non-zero (continuing)"
else
  echo "scripts/create_admin.py not found, skipping admin creation"
fi

echo "Release script completed."
