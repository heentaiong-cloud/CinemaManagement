# CinemaSystem — Deployment notes

Quick deployment notes for Railway:

- To allow the app to serve uploaded media files from the container (small projects only), add the project variable `SERVE_MEDIA` with value `true` in Railway Project > Settings > Variables. The app will then serve `MEDIA_URL` from the container filesystem during runtime.
- For production, prefer using an external object store (S3/GCS) — filesystem storage on containers is ephemeral.

Admin auto-creation:
- The release script runs `scripts/create_admin.py` during deploy; set `ADMIN_USERNAME`, `ADMIN_EMAIL`, and `ADMIN_PASSWORD` as shared variables in Railway to create the admin automatically on deploy.

S3 / Durable media storage (recommended)
---------------------------------------
For production you should use an object store (S3, DigitalOcean Spaces, GCS) so uploaded media persists across deploys. To enable S3-compatible storage:

1. Set the following environment variables in Railway Project Settings > Variables:
  - `USE_S3=true`
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_STORAGE_BUCKET_NAME`
  - Optionally `AWS_S3_REGION_NAME` and `AWS_S3_CUSTOM_DOMAIN`

2. The app uses `django-storages` and `boto3` (already added to `requirements.txt`). After setting env vars, redeploy — uploaded files will be stored in the configured bucket and served from the bucket URL.

If you'd like, I can add example settings for Google Cloud Storage instead, or wire-up common patterns (private buckets + signed URLs, CloudFront/Cloud CDN), just tell me which provider you prefer.
# Cinema Management System - Setup Instructions

A complete, production-ready Cinema Management System built with Django, featuring user authentication, movie browsing, seat selection, and ticket booking.

## 📋 Project Structure

```
CinemaSystem/
├── cinema_project/              # Project configuration
│   ├── __init__.py
│   ├── settings.py             # Django settings
│   ├── urls.py                 # URL routing
│   ├── wsgi.py                 # WSGI configuration
│   └── asgi.py                 # ASGI configuration
├── apps/
│   ├── movies/                 # Movies app
│   │   ├── migrations/
│   │   ├── models.py          # Movie, Theater, Showtime, Seat models
│   │   ├── views.py           # Movie views
│   │   ├── forms.py           # Movie forms
│   │   ├── urls.py            # Movie URLs
│   │   └── admin.py           # Admin configuration
│   └── bookings/              # Bookings app
│       ├── migrations/
│       ├── models.py          # Booking, BookingItem, Review models
│       ├── views.py           # Booking and auth views
│       ├── forms.py           # Booking forms
│       ├── urls.py            # Booking URLs
│       └── admin.py           # Admin configuration
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── home.html              # Home page
│   ├── movies/
│   │   ├── movie_list.html
│   │   └── movie_detail.html
│   ├── bookings/
│   │   ├── seat_selection.html
│   │   ├── checkout.html
│   │   ├── confirmation.html
│   │   ├── booking_history.html
│   │   ├── dashboard.html
│   │   └── add_review.html
│   └── auth/
│       ├── login.html
│       └── register.html
├── static/
│   ├── css/
│   │   └── style.css          # Main CSS styles
│   └── js/
│       └── main.js            # Main JavaScript
├── media/                      # User uploaded files
├── manage.py
├── db.sqlite3                 # SQLite database
├── requirements.txt           # Python dependencies
└── seed_data.py              # Database seeding script
```

## 🚀 Step-by-Step Setup Instructions

### Step 1: Navigate to Your Project Directory
```
cd "c:\Users\user\OneDrive\Desktop\CinemaSystem"
```

### Step 2: Create a Virtual Environment
```
python -m venv venv
```

### Step 3: Activate Virtual Environment

**On Windows (PowerShell):**
```
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```
venv\Scripts\activate.bat
```

**On macOS/Linux:**
```
source venv/bin/activate
```

### Step 4: Install Dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Apply Database Migrations
```
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create a Superuser (Admin Account)
```
python manage.py createsuperuser
```

Follow the prompts to create your admin account:
- Username: `admin`
- Email: `admin@example.com`
- Password: (choose a strong password)

### Step 7: Seed Sample Data (Optional but Recommended)
```
python manage.py shell
```

Then in the Python shell:
```python
exec(open('seed_data.py').read())
exit()
```

Or run directly:
```
python manage.py shell < seed_data.py
```

This will create:
- 8 sample movies
- 3 theaters with ~150-200 seats each
- Multiple showtimes for each movie
- Sample user accounts
- Sample reviews and bookings

### Step 8: Collect Static Files (for production-like setup)
```
python manage.py collectstatic --noinput
```

### Step 9: Run Development Server
```
python manage.py runserver
```

The server will start at: **http://127.0.0.1:8000/**

## 📱 Accessing the Application

### User Interface
- **Home Page:** `http://localhost:8000/`
- **Browse Movies:** `http://localhost:8000/movies/`
- **Login:** `http://localhost:8000/login/`
- **Register:** `http://localhost:8000/register/`
- **Dashboard:** `http://localhost:8000/bookings/dashboard/`
- **Booking History:** `http://localhost:8000/bookings/history/`

### Admin Panel
- **Admin Dashboard:** `http://localhost:8000/admin/`
- **Username:** `admin`
- **Password:** (what you set during superuser creation)

## 🎬 Features Overview

### For Users
✅ **User Authentication**
- Register new account
- Login/Logout
- User dashboard with booking history
- Profile view

✅ **Browse Movies**
- View all active movies
- Search movies by title
- Filter by genre
- View detailed movie information
- See ratings and descriptions

✅ **Booking System**
- View showtimes for each movie
- Visual seat selection (color-coded by seat type)
- Checkout review
- Instant booking confirmation
- Booking history tracking
- Leave reviews for movies

- Standard seats (₱250)
✅ **Seat Management**
- Premium seats (₱350)
- VIP seats (₱500)
- Real-time seat availability
- Visual seat map with color coding

### For Admins
✅ **Admin Panel Features**
- Manage movies (CRUD operations)
- Manage theaters/halls
- Manage showtimes
- Manage seats
- View all bookings
- View user reviews
- Monitor seat availability

## 💾 Database Models

### Movie Model
- Title, Description, Genre
- Director, Duration
- Release Date, Rating
- Poster image
- Status (Active/Archived)

### Theater Model
- Name, Location
- Total seats
- Description

### Seat Model
- Theater (FK)
- Row, Number
- Seat Type (Standard/Premium/VIP)
- Price per type

### Showtime Model
- Movie (FK)
- Theater (FK)
- Show Date & Time
- Available seats count

### Booking Model
- User (FK)
- Showtime (FK)
- Booking date
- Status (Pending/Confirmed/Cancelled)
- Total price
- Number of seats

### BookingItem Model
- Booking (FK)
- Seat (FK)
- Price at time of booking

### Review Model
- User (FK)
- Movie (FK)
- Rating (1-5 stars)
- Comment text

## 🔐 Authentication

The system uses Django's built-in authentication system with:
- User registration with email verification
- Secure password hashing
- Login/Logout functionality
- Session management
- Admin user roles

## 🛠 Technologies Used

- **Backend:** Django 4.2.7
- **Database:** SQLite (default, can be changed to PostgreSQL)
- **Frontend:** HTML5, CSS3, Bootstrap 5.3
- **JavaScript:** Vanilla JavaScript ES6
- **Image Handling:** Pillow

## 📝 Important Files Explained

### `settings.py`
- Database configuration
- Installed apps
- Static files configuration
- Template settings
- Authentication settings

### `models.py` (both apps)
- Database schema definitions
- Model relationships
- Field validations

### `views.py` (both apps)
- Class-based views for listing/detail
- Function-based views for actions
- Form processing
- Authentication decorators

### `forms.py` (both apps)
- User registration form
- Login form
- Review form
- Movie/Theater forms for admin

### `urls.py`
- URL patterns for all views
- Include statements for app URLs
- Static/media file serving

## 🎨 Customization

### Changing Colors
Edit `static/css/style.css` - look for CSS variables at the top:
```css
:root {
    --primary-color: #e74c3c;
    --secondary-color: #2c3e50;
    --accent-color: #f39c12;
}
```

### Adjusting Seat Prices
Edit `apps/movies/models.py` in the `Seat` model seed data section in `seed_data.py`

### Changing Database
Edit `cinema_project/settings.py` DATABASES configuration to use PostgreSQL or MySQL

## 📊 Sample Data Created by Seed Script

When you run the seed script, it creates:
- 8 movies with various genres
- 3 cinema theaters
- 600+ seats across all theaters
- 3 sample user accounts:
  - `john_doe` / `testpass123`
  - `jane_smith` / `testpass123`
  - `bob_wilson` / `testpass123`
- Sample bookings and reviews

## 🔧 Troubleshooting

### Issue: Module not found error
**Solution:** Make sure you've activated the virtual environment and installed requirements
```
pip install -r requirements.txt
```

### Issue: Port 8000 already in use
**Solution:** Use a different port
```
python manage.py runserver 8001
```

### Issue: Database errors
**Solution:** Reset migrations and database
```
python manage.py migrate --fake-initial
python manage.py migrate
```

### Issue: Static files not loading
**Solution:** Collect static files
```
python manage.py collectstatic --noinput
```

## 🌐 Deployment Notes

For production deployment:

1. Change `DEBUG = False` in `settings.py`
2. Update `ALLOWED_HOSTS` with your domain
3. Use a production database (PostgreSQL recommended)
4. Set a secure `SECRET_KEY`
5. Use environment variables for sensitive data
6. Configure HTTPS
7. Use Gunicorn or uWSGI as WSGI server
8. Use Nginx or Apache as reverse proxy
9. Set up proper logging
10. Configure email backend for notifications

## 📧 Contact & Support

For issues or questions about this Cinema Management System, refer to the Django documentation at https://docs.djangoproject.com/

## 📄 License

This project is provided as-is for educational and commercial use.

---

**Ready to use!** Start the server and explore the Cinema Management System. Happy booking! 🎬🎟️
