#!/usr/bin/env python
"""Create superuser for Cinema Management System"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_project.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User

# Create admin user
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'✓ Admin user created!')
    print(f'  Username: {username}')
    print(f'  Password: {password}')
    print(f'  Email: {email}')
else:
    print(f'✓ Admin user already exists!')
    print(f'  Username: {username}')
