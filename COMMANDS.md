# Cinema Management System - Quick Command Reference

## Project Setup Commands

### Initial Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Load sample data
python manage.py shell < seed_data.py
```

## Development Commands

### Running the Server
```bash
# Start development server (default port 8000)
python manage.py runserver

# Start on specific port
python manage.py runserver 8001

# Start on all interfaces (for network access)
python manage.py runserver 0.0.0.0:8000
```

### Database Operations
```bash
# Show migration status
python manage.py showmigrations

# Migrate specific app
python manage.py migrate movies

# Rollback to previous migration
python manage.py migrate movies 0001

# Create empty migration
python manage.py makemigrations --empty movies --name describe_change

# Fake migration (mark as applied without running)
python manage.py migrate --fake-initial

# Reset all migrations
python manage.py migrate movies zero
```

### Static Files
```bash
# Collect static files
python manage.py collectstatic

# Collect without prompting
python manage.py collectstatic --noinput

# Delete collected files
python manage.py collectstatic --clear

# Find static files
python manage.py findstatic css/style.css
```

### User Management
```bash
# Create superuser
python manage.py createsuperuser

# Create normal user
python manage.py shell
# Then in shell:
from django.contrib.auth.models import User
User.objects.create_user('username', 'email@example.com', 'password')
```

## Data/Shell Commands

### Django Shell
```bash
# Open Django shell
python manage.py shell

# In shell, common operations:
from apps.movies.models import Movie
from apps.bookings.models import Booking

# Query all movies
movies = Movie.objects.all()

# Query active movies
active_movies = Movie.objects.filter(status='active')

# Get single movie
movie = Movie.objects.get(id=1)

# Create movie
movie = Movie.objects.create(
    title='Test Movie',
    description='Test',
    genre='Action',
    duration=120,
    release_date='2025-12-01'
)

# Update movie
movie.title = 'New Title'
movie.save()

# Delete movie
movie.delete()

# Count movies
count = Movie.objects.count()
```

### Management Commands
```bash
# Run specific management command
python manage.py <command>

# Get help for command
python manage.py <command> --help

# List all commands
python manage.py help
```

## Testing Commands

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.movies

# Run specific test class
python manage.py test apps.movies.tests.MovieTestCase

# Run specific test method
python manage.py test apps.movies.tests.MovieTestCase.test_movie_creation

# Run with verbose output
python manage.py test --verbose=2

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

## Clean up Commands

```bash
# Remove all pyc files
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete

# Remove all migrations except __init__.py
# (CAREFUL - use only if needed)
# find ./apps/*/migrations/ -name "*.py" -not -name "__init__.py" -delete

# Clear cache
python manage.py clear_cache

# Remove orphaned media files
python manage.py cleanupfilestamps
```

## Admin Commands

```bash
# Change user password
python manage.py changepassword username

# Remove user (in shell)
from django.contrib.auth.models import User
user = User.objects.get(username='username')
user.delete()

# Make user superuser (in shell)
from django.contrib.auth.models import User
user = User.objects.get(username='username')
user.is_staff = True
user.is_superuser = True
user.save()
```

## Debugging Commands

```bash
# Run Django debug toolbar checks
python manage.py debug_toolbar check

# Display SQL queries (in shell)
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as context:
    # Your code
    pass
print(context.captured_queries)

# Print SQL query for a QuerySet (in shell)
from django.db import connection
movies = Movie.objects.all()
print(movies.query)
```

## Production Commands

```bash
# Collect all static files for production
python manage.py collectstatic --noinput

# Check for deployment issues
python manage.py check --deploy

# Create backup
python manage.py dumpdata > backup.json

# Restore from backup
python manage.py loaddata backup.json

# Export specific app data
python manage.py dumpdata apps.movies > movies_backup.json

# Generate secret key
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

## Useful Shortcuts

### Windows
```batch
# Activate venv and start server (create as .bat file)
@echo off
call venv\Scripts\activate.bat && python manage.py runserver
```

### macOS/Linux
```bash
# Activate venv and start server (create as .sh file)
#!/bin/bash
source venv/bin/activate && python manage.py runserver
```

## Common Issues & Solutions

### Port Already in Use
```bash
# Find process using port 8000
# Windows: netstat -ano | findstr :8000
# Linux/Mac: lsof -i :8000

# Use different port
python manage.py runserver 8001
```

### Database Locked
```bash
# Remove database and recreate
rm db.sqlite3
python manage.py migrate
```

### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput
```

### ImportError
```bash
# Reinstall packages
pip install -r requirements.txt --upgrade
```

## URL Patterns

### Development
- Home: `http://localhost:8000/`
- Movies: `http://localhost:8000/movies/`
- Admin: `http://localhost:8000/admin/`
- Movie Detail: `http://localhost:8000/movie/1/`
- Search: `http://localhost:8000/search/?q=keyword`
- Login: `http://localhost:8000/login/`
- Register: `http://localhost:8000/register/`
- Dashboard: `http://localhost:8000/bookings/dashboard/`
- Booking History: `http://localhost:8000/bookings/history/`

## Environment Variables

```bash
# Set environment variables (Windows PowerShell)
$env:DEBUG = "True"
$env:SECRET_KEY = "your-secret-key"

# Set environment variables (Linux/Mac)
export DEBUG=True
export SECRET_KEY="your-secret-key"

# Load from .env file (install python-dotenv)
pip install python-dotenv
```

### Updated settings.py
```python
from decouple import config

DEBUG = config('DEBUG', default=True, cast=bool)
SECRET_KEY = config('SECRET_KEY', default='dev-key')
```

## Deployement Checklist

- [ ] Set `DEBUG = False` in settings.py
- [ ] Update `ALLOWED_HOSTS`
- [ ] Set secure `SECRET_KEY`
- [ ] Configure database (PostgreSQL recommended)
- [ ] Run `python manage.py check --deploy`
- [ ] Collect static files
- [ ] Configure email backend
- [ ] Set up HTTPS/SSL
- [ ] Configure logging
- [ ] Set up backup strategy
- [ ] Test error pages
- [ ] Configure CORS if needed
- [ ] Set up monitoring
- [ ] Create deployment documentation

---

**Tip:** Save these commands in a cheat sheet or create shell scripts for frequently used operations!
