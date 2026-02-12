from django.urls import path
from . import views

urlpatterns = [
    path('seat-selection/<int:showtime_id>/', views.SeatSelectionView.as_view(), name='seat_selection'),
    path('checkout/<int:showtime_id>/', views.BookingCheckoutView.as_view(), name='checkout'),
    path('confirmation/<int:booking_id>/', views.BookingConfirmationView.as_view(), name='booking_confirmation'),
    path('ticket/<int:booking_id>/', views.download_ticket, name='download_ticket'),
    path('history/', views.BookingHistoryView.as_view(), name='booking_history'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('api/seat-availability/<int:showtime_id>/', views.get_seat_availability, name='seat_availability'),
    path('add-review/<int:movie_id>/', views.add_review, name='add_review'),
]
