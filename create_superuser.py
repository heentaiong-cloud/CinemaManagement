"""
Create a superuser account for Django admin
"""
from django.contrib.auth.models import User
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_project.settings')
django.setup()

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print("✓ Admin superuser created successfully")
    print("  Username: admin")
    print("  Email: admin@example.com")
    print("  Password: admin123")
else:
    print("✓ Admin superuser already exists")
