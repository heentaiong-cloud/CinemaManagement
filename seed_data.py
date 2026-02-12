"""
Seed script to populate sample data into the database.
Run with: python manage.py shell < seed_data.py
"""

from django.utils import timezone
from datetime import datetime, timedelta
from apps.movies.models import Movie, Theater, Showtime, Seat
from apps.bookings.models import Review, Booking, BookingItem
from django.contrib.auth.models import User

print("Starting database seed...")

# Clear existing data
Movie.objects.all().delete()
Theater.objects.all().delete()
Showtime.objects.all().delete()
Seat.objects.all().delete()
Review.objects.all().delete()
Booking.objects.all().delete()
BookingItem.objects.all().delete()

# Create sample movies
# Create sample movies
movies_data = [
    {
        'title': 'The Quantum Paradox',
        'description': 'A mind-bending sci-fi thriller about time travel and alternate realities. A physicist discovers a way to manipulate quantum states and must prevent a catastrophic timeline collapse.',
        'genre': 'Sci-Fi',
        'director': 'Christopher Nolan',
        'duration': 148,
        'release_date': datetime(2025, 12, 15).date(),
        'rating': 8.5,
        'status': 'active',
    },
    {
        'title': 'Love in Paris',
        'description': 'A romantic drama set in the City of Light. Two souls from different worlds meet and discover that love knows no boundaries.',
        'genre': 'Romance',
        'director': 'Wes Anderson',
        'duration': 120,
        'release_date': datetime(2025, 11, 20).date(),
        'rating': 7.8,
        'status': 'active',
    },
    {
        'title': 'Dark Shadows',
        'description': 'A gripping thriller where a detective must solve a series of murders while uncovering dark secrets of a small town.',
        'genre': 'Thriller',
        'director': 'Denis Villeneuve',
        'duration': 135,
        'release_date': datetime(2025, 10, 30).date(),
        'rating': 8.1,
        'status': 'active',
    },
    {
        'title': 'Space Odyssey 2050',
        'description': 'An epic space adventure following a team of astronauts on a mission to explore a distant galaxy and discover alien civilizations.',
        'genre': 'Sci-Fi',
        'director': 'James Cameron',
        'duration': 160,
        'release_date': datetime(2025, 12, 20).date(),
        'rating': 8.7,
        'status': 'active',
    },
    {
        'title': 'Laugh Out Loud',
        'description': 'A hilarious comedy following three friends as they navigate life, relationships, and unexpected adventures in the city.',
        'genre': 'Comedy',
        'director': 'Judd Apatow',
        'duration': 95,
        'release_date': datetime(2025, 11, 10).date(),
        'rating': 7.5,
        'status': 'active',
    },
    {
        'title': 'Dragon Chronicles',
        'description': 'A fantasy epic where a young hero must defeat an ancient dragon to save the kingdom and restore peace to the realm.',
        'genre': 'Fantasy',
        'director': 'Peter Jackson',
        'duration': 170,
        'release_date': datetime(2025, 12, 1).date(),
        'rating': 8.9,
        'status': 'active',
    },
    {
        'title': 'The Last Heist',
        'description': 'A crime drama about a master thief planning one last spectacular heist to retire. Everything goes wrong when unexpected forces interfere.',
        'genre': 'Crime',
        'director': 'Steven Soderbergh',
        'duration': 125,
        'release_date': datetime(2025, 11, 5).date(),
        'rating': 8.0,
        'status': 'active',
    },
    {
        'title': 'Ocean\'s Mystery',
        'description': 'An underwater adventure exploring mysterious creatures and lost civilizations at the bottom of the ocean.',
        'genre': 'Adventure',
        'director': 'James Wan',
        'duration': 130,
        'release_date': datetime(2025, 12, 5).date(),
        'rating': 8.3,
        'status': 'active',
    },
]

movies = []
for movie_data in movies_data:
    movie = Movie.objects.create(**movie_data)
    movies.append(movie)
    print(f"✓ Created movie: {movie.title}")

# Create sample theaters
theaters_data = [
    {
        'name': 'Central Cinema Hall',
        'location': '123 Main Street, Downtown',
        'total_seats': 150,
    },
    {
        'name': 'Sunset Theatre',
        'location': '456 Oak Avenue, Westside',
        'total_seats': 200,
    },
    {
        'name': 'Starlight Cineplex',
        'location': '789 Park Road, Eastside',
        'total_seats': 180,
    },
]

theaters = []
for theater_data in theaters_data:
    theater = Theater.objects.create(**theater_data)
    theaters.append(theater)
    print(f"✓ Created theater: {theater.name}")

# Create seats for each theater
for theater in theaters:
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    seats_per_row = theater.total_seats // len(rows)
    
    for row_idx, row in enumerate(rows):
        for col_num in range(1, seats_per_row + 1):
            # VIP seats (middle rows, middle seats)
            if row in ['D', 'E', 'F'] and seats_per_row // 3 <= col_num <= 2 * seats_per_row // 3:
                seat_type = 'vip'
            # Premium seats (middle rows)
            elif row in ['C', 'D', 'E', 'F', 'G']:
                seat_type = 'premium'
            # Standard seats
            else:
                seat_type = 'standard'
            
            seat_number = f"{row}{col_num}"
            Seat.objects.create(
                theater=theater,
                row=row,
                column=col_num,
                seat_number=seat_number,
                seat_type=seat_type,
            )
    print(f"✓ Created {theater.total_seats} seats for {theater.name}")

# Create showtimes
showtime_count = 0
for movie in movies:
    for theater in theaters:
        # Create 3 showtimes per movie per theater (next 7 days)
        for day_offset in range(0, 7, 3):
            show_date = (datetime.now() + timedelta(days=day_offset)).date()
            
            for time_slot in ['10:30', '14:00', '18:30', '21:00']:
                time_parts = time_slot.split(':')
                show_time = timezone.datetime.strptime(time_slot, '%H:%M').time()
                
                # Base ticket price is 300, but can vary
                ticket_price = 300.00
                
                showtime = Showtime.objects.create(
                    movie=movie,
                    theater=theater,
                    show_date=show_date,
                    show_time=show_time,
                    ticket_price=ticket_price,
                    available_seats=theater.total_seats,
                )
                showtime_count += 1

print(f"✓ Created {showtime_count} showtimes")

# Create sample users
users_data = [
    {
        'username': 'john_doe',
        'email': 'john@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'password': 'testpass123',
    },
    {
        'username': 'jane_smith',
        'email': 'jane@example.com',
        'first_name': 'Jane',
        'last_name': 'Smith',
        'password': 'testpass123',
    },
    {
        'username': 'bob_wilson',
        'email': 'bob@example.com',
        'first_name': 'Bob',
        'last_name': 'Wilson',
        'password': 'testpass123',
    },
]

users = []
for user_data in users_data:
    password = user_data.pop('password')
    user = User.objects.create_user(**user_data, password=password)
    users.append(user)
    print(f"✓ Created user: {user.username}")

# Create sample reviews
for movie in movies[:3]:
    for user in users[:2]:
        review = Review.objects.create(
            movie=movie,
            user=user,
            rating=7 + (hash(f"{movie.id}{user.id}") % 3),
            comment=f"Great movie! {user.first_name} really enjoyed watching {movie.title}.",
        )
print("✓ Created reviews")

# Create sample bookings
from decimal import Decimal
for user in users:
    for i, showtime in enumerate(Showtime.objects.all()[:2]):
        # Get some available seats
        available_seats = Seat.objects.filter(theater=showtime.theater)[:3]
        
        booking = Booking.objects.create(
            user=user,
            showtime=showtime,
            status='confirmed',
        )
        
        total_price = Decimal('0.00')
        for seat in available_seats:
            BookingItem.objects.create(
                booking=booking,
                showtime=showtime,
                seat=seat,
                price=showtime.ticket_price,
            )
            total_price += showtime.ticket_price
        
        booking.total_price = total_price
        booking.number_of_seats = available_seats.count()
        booking.save()

print("✓ Created bookings")

print("\n✅ Database seed complete!")
print(f"Sample Users:")
for user in users:
    print(f"  Username: {user.username}, Password: testpass123")
