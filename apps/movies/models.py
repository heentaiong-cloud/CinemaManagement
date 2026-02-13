from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    """Movie model"""
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    duration = models.IntegerField()  # in minutes
    rating = models.FloatField(default=0)  # IMDb-like rating
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    release_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-release_date']
        
    def __str__(self):
        return self.title


class Theater(models.Model):
    """Theater/Cinema Hall model"""
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    total_seats = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Theaters"
    
    def __str__(self):
        return self.name


class Showtime(models.Model):
    """Showtime model linking movies to theaters with specific times"""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='showtimes')
    show_date = models.DateField()
    show_time = models.TimeField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    available_seats = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['show_date', 'show_time']
        unique_together = ['movie', 'theater', 'show_date', 'show_time']
    
    def __str__(self):
        return f"{self.movie.title} at {self.theater.name} - {self.show_date} {self.show_time}"
    
    def get_available_seats(self):
        """Get count of available seats for this showtime"""
        from apps.bookings.models import BookingItem
        # Total seats in the theater (fallback to counting Seat objects)
        try:
            total = self.theater.total_seats
        except Exception:
            from apps.movies.models import Seat as SeatModel
            total = SeatModel.objects.filter(theater=self.theater).count()
        booked = BookingItem.objects.filter(showtime=self).count()
        return max(total - booked, 0)
    
    def update_available_seats(self):
        """Update available seats count"""
        self.available_seats = self.get_available_seats()
        self.save()

    def save(self, *args, **kwargs):
        """Auto-fill available_seats on create if not provided.

        This helps the admin form where `available_seats` may be left empty.
        """
        # If creating and available_seats is falsy, initialize from theater total
        if not self.pk and (self.available_seats is None or self.available_seats == 0):
            try:
                total = self.theater.total_seats
            except Exception:
                total = Seat.objects.filter(theater=self.theater).count()
            self.available_seats = total
        super().save(*args, **kwargs)


class Seat(models.Model):
    """Seat model for each theater"""
    SEAT_TYPE_CHOICES = [
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('vip', 'VIP'),
    ]
    
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)  # e.g., "A1", "B5"
    row = models.CharField(max_length=5)
    column = models.IntegerField()
    seat_type = models.CharField(max_length=20, choices=SEAT_TYPE_CHOICES, default='standard')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['theater', 'seat_number']
        ordering = ['row', 'column']
    
    def __str__(self):
        return f"{self.theater.name} - {self.seat_number}"

    @property
    def number(self):
        """Numeric part of the seat (column) for templates"""
        return self.column
