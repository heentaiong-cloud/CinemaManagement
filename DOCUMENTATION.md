# Cinema Management System - Complete Documentation

## 📖 Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage Guide](#usage-guide)
7. [API Endpoints](#api-endpoints)
8. [Admin Panel Guide](#admin-panel-guide)
9. [Database Schema](#database-schema)
10. [Customization Guide](#customization-guide)

## Project Overview

Cinema Management System is a complete Django web application that allows users to:
- Browse movies and showtimes
- Select seats visually
- Book movie tickets
- Manage their bookings
- Leave reviews

Administrators can manage movies, theaters, showtimes, and view all bookings.

**Stack:**
- Python 3.8+
- Django 4.2.7
- SQLite (replaceable with PostgreSQL/MySQL)
- Bootstrap 5.3
- HTML5/CSS3/JavaScript ES6

## Architecture

### Project Structure
```
CinemaSystem/
├── cinema_project/          # Project settings
├── apps/
│   ├── movies/             # Movies app
│   └── bookings/           # Bookings & Auth app
├── templates/              # HTML templates
├── static/                 # CSS, JS, images
├── media/                  # User uploads
└── manage.py
```

### App Architecture

#### Movies App
- **Models:** Movie, Theater, Showtime, Seat
- **Views:** Movie list, Movie detail, Movie search
- **Admin Interface:** Full CRUD for movies, theaters, showtimes, seats

#### Bookings App
- **Models:** Booking, BookingItem, Review
- **Views:** Authentication, Seat selection, Checkout, Booking confirmation
- **Features:** User registration, login, booking history, dashboard

## Features

### User Features
1. **Authentication**
   - User registration with email validation
   - Secure login/logout
   - Session management
   - User dashboard

2. **Movie Browsing**
   - Browse all active movies
   - Search by title or keywords
   - Filter by genre
   - View detailed information with ratings
   - See movie posters

3. **Booking System**
   - View available showtimes
   - Visual seat selection with color coding
   - Real-time seat availability
   - Instant booking confirmation
   - Booking history with details

4. **Review System**
   - Leave 1-5 star reviews
   - Add comments/feedback
   - View community reviews

### Admin Features
1. **Movie Management**
   - Create, read, update, delete movies
   - Manage movie details, ratings, posters
   - Control active status

2. **Theater Management**
   - Create and manage theaters
   - Configure seat layout
   - Set seat prices by type

3. **Showtime Management**
   - Create showtimes for movies
   - Set show dates and times
   - Track available seats

4. **Booking Management**
   - View all bookings
   - See customer details
   - Track booking status
   - View seat assignments

5. **Analytics Dashboard**
   - View all reviews
   - Monitor system usage
   - Track bookings

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step-by-Step Installation

1. **Clone/Extract Project**
   ```
   # Navigate to project directory
   cd CinemaSystem
   ```

2. **Create Virtual Environment**
   ```
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

5. **Run Migrations**
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Admin User**
   ```
   python manage.py createsuperuser
   ```

7. **Load Sample Data (Optional)**
   ```
   python manage.py shell < seed_data.py
   ```

8. **Start Development Server**
   ```
   python manage.py runserver
   ```

Access at: http://localhost:8000

## Configuration

### settings.py

**Database Configuration:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**For PostgreSQL:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cinema_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**Static Files:**
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

**Media Files:**
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**Authentication:**
```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
```

## Usage Guide

### For End Users

#### Registration & Login
1. Click "Register" button
2. Fill in username, email, password
3. Click "Register"
4. Login with credentials
5. Access your dashboard

#### Browsing Movies
1. Click "Movies" in navigation
2. Browse all movies
3. Use search or filters
4. Click "View Details" for more info

#### Booking Tickets
1. View movie details
2. Select a showtime
3. Click "Book Now"
4. Select your seats (visual seating chart)
5. Review total price
6. Proceed to checkout
7. Confirm booking
8. Download/print confirmation

#### Managing Bookings
1. Click "My Bookings"
2. View all your bookings
3. See confirmation numbers
4. Check seat assignments
5. View booking dates and times

#### Leaving Reviews
1. Go to movie detail page
2. Click "Add Your Review"
3. Rate the movie (1-5 stars)
4. Add optional comment
5. Submit review
6. See your review on the page

### For Administrators

#### Accessing Admin Panel
1. Go to: `/admin/`
2. Login with superuser credentials
3. Access all management interfaces

#### Managing Movies
1. Admin → Movies → Add Movie
2. Fill in all details
3. Upload poster image
4. Set as active/inactive
5. Save

#### Adding Showtimes
1. Admin → Showtimes → Add Showtime
2. Select movie and theater
3. Set date and time
4. System auto-calculates available seats
5. Save

#### Viewing Bookings
1. Admin → Bookings
2. See all customer bookings
3. Filter by date, movie, status
4. View booking details
5. Confirm or cancel if needed

## API Endpoints

### Public Endpoints
```
GET     /                           # Homepage
GET     /movies/                    # All movies
GET     /movie/<id>/               # Movie details
POST    /search/                    # Search movies
POST    /register/                  # User registration
POST    /login/                     # User login
GET     /logout/                    # User logout
```

### Authenticated Endpoints
```
GET     /bookings/seat-selection/<showtime_id>/   # Select seats
GET     /bookings/checkout/<showtime_id>/         # Checkout
POST    /bookings/checkout/<showtime_id>/         # Complete booking
GET     /bookings/confirmation/<id>/              # Booking confirmation
GET     /bookings/history/                        # Booking history
GET     /bookings/dashboard/                      # User dashboard
POST    /bookings/add-review/<movie_id>/          # Add review
```

### API Endpoints
```
GET     /bookings/api/seat-availability/<showtime_id>/   # Seat availability
```

## Admin Panel Guide

### Movies Section
- **List Movies:** View all movies with filters
- **Add Movie:** Create new movie entry
- **Edit Movie:** Update movie details
- **Delete Movie:** Remove movie
- **Bulk Actions:** Edit multiple movies

Fields:
- Title, Description, Genre
- Director, Duration, Release Date
- Rating (0-10)
- Poster image
- Status (Active/Archived)

### Theaters Section
- **List Theaters:** View all cinema halls
- **Add Theater:** Create new theater
- **Edit Theater:** Update theater details
- **Manage Seats:** Configure seat layout

Fields:
- Name, Location, Total Seats
- Description, Created Date

### Showtimes Section
- **List Showtimes:** View all showtimes
- **Add Showtime:** Schedule new showtime
- **Edit Showtime:** Modify existing showtime
- **Available Seats:** Monitor seat availability

Fields:
- Movie, Theater, Date, Time
- Available Seats (auto-updated)
- Ticket Price

### Bookings Section
- **View All Bookings:** List customer bookings
- **Search Bookings:** Filter by user, movie, date
- **Booking Details:** See seats, prices, status
- **Status Management:** Update booking status

### Reviews Section
- **View Reviews:** All movie reviews
- **Filter Reviews:** By movie, rating, user
- **Manage Reviews:** Edit or delete inappropriate reviews

## Database Schema

### Movie
```
- id (PK)
- title (CharField)
- description (TextField)
- genre (CharField)
- duration (IntegerField)
- release_date (DateField)
- rating (DecimalField)
- poster (ImageField)
- status (CharField) - use 'active' for visible movies
- created_at (DateTimeField)
- updated_at (DateTimeField)
```

### Theater
```
- id (PK)
- name (CharField)
- location (CharField)
- total_seats (IntegerField)
- description (TextField)
- created_at (DateTimeField)
```

### Seat
```
- id (PK)
- theater_id (FK)
- row (CharField)
- number (IntegerField)
- seat_type (CharField) # standard, premium, vip
- price (DecimalField)
- unique_together: (theater, row, number)
```

### Showtime
```
- id (PK)
- movie_id (FK)
- theater_id (FK)
- show_date (DateField)
- show_time (TimeField)
- available_seats (IntegerField)
- created_at (DateTimeField)
- unique_together: (movie, theater, show_date, show_time)
```

### Booking
```
- id (PK)
- user_id (FK)
- showtime_id (FK)
- booking_date (DateTimeField)
- status (CharField) # pending, confirmed, cancelled
- total_price (DecimalField)
- number_of_seats (IntegerField)
```

### BookingItem
```
- id (PK)
- booking_id (FK)
- showtime_id (FK)
- seat_id (FK)
- price (DecimalField)
- booked_at (DateTimeField)
- unique_together: (booking, seat)
```

### Review
```
- id (PK)
- movie_id (FK)
- user_id (FK)
- rating (IntegerField) # 1-5
- comment (TextField)
- created_at (DateTimeField)
- updated_at (DateTimeField)
- unique_together: (movie, user)
```

## Customization Guide

### Changing Theme Colors

Edit `static/css/style.css`:
```css
:root {
    --primary-color: #e74c3c;        /* Red - Main color */
    --secondary-color: #2c3e50;      /* Dark blue - Secondary */
    --accent-color: #f39c12;         /* Orange - Accents */
}
```

### Adding New Features

1. **Create New View:**
   ```python
   # In apps/movies/views.py
   from django.views import View
   
   class CustomView(View):
       def get(self, request):
           # Your logic
           return render(request, 'template.html')
   ```

2. **Add URL:**
   ```python
   # In urls.py
   path('custom/', views.CustomView.as_view(), name='custom')
   ```

3. **Create Template:**
   ```html
   <!-- In templates/ -->
   {% extends 'base.html' %}
   {% block content %}
   <!-- Your HTML -->
   {% endblock %}
   ```

### Using Different Database

1. Install database driver:
   ```
   pip install psycopg2-binary  # For PostgreSQL
   ```

2. Update `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'cinema_db',
           'USER': 'user',
           'PASSWORD': 'password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. Run migrations:
   ```
   python manage.py migrate
   ```

### Adding Payment Gateway

1. Install payment library:
   ```
   pip install stripe
   ```

2. Add to `settings.py`:
   ```python
   STRIPE_PUBLIC_KEY = 'your-public-key'
   STRIPE_SECRET_KEY = 'your-secret-key'
   ```

3. Create payment view in bookings app
4. Update checkout.html with payment form

### Email Configuration

Update `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## Performance Optimization

### Database Optimization
```python
# Use select_related for foreign keys
movies = Movie.objects.select_related('user').all()

# Use prefetch_related for reverse relations
bookings = Booking.objects.prefetch_related('items').all()
```

### Caching
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def movie_list(request):
    pass
```

### Query Optimization
- Use `.only()` and `.defer()` for large models
- Add database indexes for frequently queried fields
- Use pagination for large datasets

## Troubleshooting

### Issue: Migrations not working
```bash
python manage.py migrate --fake-initial
python manage.py migrate
```

### Issue: Static files not loading
```bash
python manage.py collectstatic --noinput
```

### Issue: Import errors
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Database locked
```bash
rm db.sqlite3
python manage.py migrate
```

## Support & Resources

- Django Documentation: https://docs.djangoproject.com/
- Bootstrap Documentation: https://getbootstrap.com/docs/5.3/
- SQLite Documentation: https://www.sqlite.org/docs.html
- Django REST Framework: https://www.django-rest-framework.org/

---

**Happy Coding!** 🎬
