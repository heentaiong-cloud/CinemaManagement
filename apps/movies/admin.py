from django.contrib import admin
from django.utils.html import format_html, format_html_join
from apps.bookings.models import BookingItem
from .models import Movie, Theater, Showtime, Seat


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'director', 'status', 'release_date']
    list_filter = ['status', 'genre', 'release_date']
    search_fields = ['title', 'director']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'genre', 'director', 'duration', 'release_date')
        }),
        ('Details', {
            'fields': ('description', 'rating', 'status', 'poster')
        }),
    )


@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'total_seats']
    search_fields = ['name', 'location']


@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ['movie', 'theater', 'show_date', 'show_time', 'available_seats', 'booked_seats_count', 'ticket_price']
    list_filter = ['show_date', 'theater', 'movie']
    search_fields = ['movie__title', 'theater__name']
    readonly_fields = ['available_seats', 'booked_seats_list']
    inlines = []

    def booked_seats_count(self, obj):
        return BookingItem.objects.filter(showtime=obj).count()
    booked_seats_count.short_description = 'Booked Seats'

    def booked_seats_list(self, obj):
        items = BookingItem.objects.filter(showtime=obj).select_related('seat')
        if not items.exists():
            return '-'
        # render small badges for each booked seat
        html = format_html_join('',
            '<span style="display:inline-block;margin:2px;padding:4px 8px;border-radius:6px;background:#f1f5f9;color:#0f1724;font-weight:600;">{}</span>',
            ((f"{it.seat.row}{it.seat.number}" ,) for it in items)
        )
        return format_html(html)
    booked_seats_list.short_description = 'Booked Seats (list)'


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['seat_number', 'theater', 'row', 'seat_type']
    list_filter = ['seat_type', 'theater']
    search_fields = ['seat_number', 'theater__name', 'row']
