from django.db import models
from django.contrib.auth.models import User
from apps.movies.models import Showtime, Seat
from decimal import Decimal


class Booking(models.Model):
    """Booking model for customer bookings"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    number_of_seats = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-booking_date']
    
    def __str__(self):
        return f"Booking #{self.id} - {self.user.username} - {self.showtime.movie.title}"
    
    def calculate_total(self):
        """Calculate total price from booking items"""
        total = sum(float(item.price) for item in self.items.all())
        self.total_price = Decimal(str(total))
        self.number_of_seats = self.items.count()
        self.save()
        return self.total_price


class BookingItem(models.Model):
    """Individual seat booking"""
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='items')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    booked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['booking', 'seat']
    
    def __str__(self):
        return f"{self.booking} - {self.seat}"


class Review(models.Model):
    """Movie review model"""
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['movie', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
