#!/usr/bin/env python3
"""Create a superuser from environment variables.

Usage (recommended on server):
  ADMIN_USERNAME=admin ADMIN_EMAIL=admin@example.com ADMIN_PASSWORD=ChangeMe123 python scripts/create_admin.py

The script will not overwrite an existing user.
"""
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_project.settings')
    try:
        import django
        django.setup()
    except Exception as exc:
        print('Failed to setup Django:', exc)
        sys.exit(1)

    from django.contrib.auth import get_user_model

    User = get_user_model()
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
    password = os.environ.get('ADMIN_PASSWORD', 'ChangeMe123')

    if User.objects.filter(username=username).exists():
        print(f"Superuser '{username}' already exists.")
        return

    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Created superuser '{username}' with email '{email}'.")


if __name__ == '__main__':
    main()
