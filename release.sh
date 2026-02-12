#!/usr/bin/env bash
set -euo pipefail

echo "Starting release script..."

# Activate venv if created by the build process
if [ -f /app/.venv/bin/activate ]; then
  . /app/.venv/bin/activate
fi

# Ensure STATIC_ROOT exists (safety for WhiteNoise)
python - <<'PY'
from django.conf import settings
import os

static_root = getattr(settings, 'STATIC_ROOT', 'staticfiles')
os.makedirs(static_root, exist_ok=True)
print('Ensured STATIC_ROOT:', static_root)
PY

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Release script completed."
