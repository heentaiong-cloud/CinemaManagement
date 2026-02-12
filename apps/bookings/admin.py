from django.contrib import admin
from .models import Booking, BookingItem, Review


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'showtime', 'status', 'total_price', 'booking_date')
    list_filter = ('status', 'booking_date', 'showtime__movie')
    search_fields = ('user__username', 'showtime__movie__title')
    readonly_fields = ('booking_date', 'total_price', 'number_of_seats')
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('id', 'user', 'showtime', 'booking_date')
        }),
        ('Details', {
            'fields': ('number_of_seats', 'total_price', 'status')
        }),
    )


@admin.register(BookingItem)
class BookingItemAdmin(admin.ModelAdmin):
    list_display = ('booking', 'seat', 'price', 'booked_at')
    list_filter = ('booked_at', 'seat__seat_type')
    search_fields = ('booking__user__username', 'seat__row')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'movie__title')
