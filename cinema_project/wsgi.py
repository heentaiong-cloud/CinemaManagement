"""
WSGI config for cinema_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/
"""

import os

# Set the default settings module early
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_project.settings')

from django.core.wsgi import get_wsgi_application

# Ensure STATIC_ROOT exists to avoid WhiteNoise warnings when container starts
try:
	from django.conf import settings
	static_root = getattr(settings, 'STATIC_ROOT', None)
	if static_root:
		os.makedirs(static_root, exist_ok=True)
except Exception:
	# best-effort; avoid failing startup for missing dirs
	pass

application = get_wsgi_application()
