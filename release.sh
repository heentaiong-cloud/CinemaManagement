#!/usr/bin/env bash
set -e

# Create static root dir (defensive)
python - <<PY
from django.conf import settings
import os
if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
    os.makedirs(settings.STATIC_ROOT, exist_ok=True)
PY

# Run migrations and collectstatic non-interactively
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear

echo "Release tasks completed"
