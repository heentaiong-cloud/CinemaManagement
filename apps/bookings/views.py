from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from decimal import Decimal
from datetime import datetime

from apps.movies.models import Showtime, Seat, Theater
from .models import Booking, BookingItem, Review
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ReviewForm
from django.http import HttpResponse
from io import BytesIO

try:
    from PIL import Image, ImageDraw, ImageFont
except Exception:
    Image = None


class RegisterView(View):
    """User registration view"""
    template_name = 'auth/register.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form, 'page': 'register'})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form, 'page': 'register'})


class LoginView(View):
    """User login view"""
    template_name = 'auth/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = CustomAuthenticationForm()
        return render(request, self.template_name, {'form': form, 'page': 'login'})
    
    def post(self, request):
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
        return render(request, self.template_name, {'form': form, 'page': 'login'})


class LogoutView(View):
    """User logout view"""
    def get(self, request):
        logout(request)
        return redirect('home')

    def post(self, request):
        # support POST logout from hidden form
        logout(request)
        return redirect('home')


class SeatSelectionView(LoginRequiredMixin, View):
    """Seat selection for booking"""
    template_name = 'bookings/seat_selection.html'
    login_url = 'login'
    
    def get(self, request, showtime_id):
        showtime = get_object_or_404(Showtime, id=showtime_id)
        seats = Seat.objects.filter(theater=showtime.theater)
        
        # Get booked seats
        booked_seats = BookingItem.objects.filter(
            showtime=showtime
        ).values_list('seat_id', flat=True)
        
        # Organize seats by row
        seats_by_row = {}
        for seat in seats:
            if seat.row not in seats_by_row:
                seats_by_row[seat.row] = []
            seat.is_booked = seat.id in booked_seats
            seats_by_row[seat.row].append(seat)
        
        context = {
            'showtime': showtime,
            'seats_by_row': sorted(seats_by_row.items()),
            'page': 'seat_selection',
        }
        return render(request, self.template_name, context)


class BookingCheckoutView(LoginRequiredMixin, View):
    """Booking checkout view"""
    template_name = 'bookings/checkout.html'
    login_url = 'login'
    
    def get(self, request, showtime_id):
        showtime = get_object_or_404(Showtime, id=showtime_id)
        # Accept either repeated ?seats=1&seats=2 or comma-separated ?seats=1,2,3
        raw_seats = request.GET.getlist('seats') or request.GET.get('seats', '')

        # Normalize into list of ID strings
        if isinstance(raw_seats, list):
            # flatten any comma-separated entries
            flat = []
            for entry in raw_seats:
                flat.extend([s for s in str(entry).split(',') if s.strip()])
            seat_id_strs = flat
        else:
            seat_id_strs = [s for s in str(raw_seats).split(',') if s.strip()]

        if not seat_id_strs:
            return redirect('movie_detail', pk=showtime.movie.id)

        try:
            seat_ids = [int(s) for s in seat_id_strs]
        except ValueError:
            return redirect('movie_detail', pk=showtime.movie.id)

        seats = Seat.objects.filter(id__in=seat_ids)
        # price per seat comes from showtime ticket_price
        total_price = showtime.ticket_price * seats.count()
        
        context = {
            'showtime': showtime,
            'seats': seats,
            'total_price': total_price,
            'seat_ids': ','.join(str(s) for s in seat_ids),
            'page': 'checkout',
        }
        return render(request, self.template_name, context)
    
    @transaction.atomic
    def post(self, request, showtime_id):
        showtime = get_object_or_404(Showtime, id=showtime_id)
        raw = request.POST.get('seat_ids', '')
        seat_id_strs = [s for s in str(raw).split(',') if s.strip()]

        if not seat_id_strs:
            return redirect('movie_detail', pk=showtime.movie.id)

        try:
            seat_ids = [int(s) for s in seat_id_strs]
        except ValueError:
            return render(request, self.template_name, {
                'error': 'Invalid seat selection.',
                'showtime': showtime,
            })

        seats = Seat.objects.filter(id__in=seat_ids)
        
        # Check if seats are still available
        booked_seats = BookingItem.objects.filter(
            showtime=showtime,
            seat__in=seats
        ).exists()
        
        if booked_seats:
            # Seat no longer available
            return render(request, self.template_name, {
                'error': 'One or more seats are no longer available. Please select again.',
                'showtime': showtime,
            })
        
        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            showtime=showtime,
            status='confirmed'
        )
        
        # Create booking items using showtime ticket_price
        total_price = Decimal(str(showtime.ticket_price)) * seats.count()
        for seat in seats:
            BookingItem.objects.create(
                booking=booking,
                showtime=showtime,
                seat=seat,
                price=showtime.ticket_price
            )
        
        booking.total_price = total_price
        booking.number_of_seats = seats.count()
        booking.save()
        
        # Update available seats
        showtime.available_seats = showtime.get_available_seats()
        showtime.save()
        
        return redirect('booking_confirmation', booking_id=booking.id)


class BookingConfirmationView(LoginRequiredMixin, View):
    """Booking confirmation view"""
    template_name = 'bookings/confirmation.html'
    login_url = 'login'
    
    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        context = {
            'booking': booking,
            'page': 'confirmation',
        }
        return render(request, self.template_name, context)


def download_ticket(request, booking_id):
    """Generate a simple ticket image (PNG) and return as download.

    Uses Pillow (PIL) which is in requirements. If Pillow is missing, return 404.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    # ensure only owner or staff can download
    if not request.user.is_authenticated or (booking.user != request.user and not request.user.is_staff):
        return redirect('login')

    if Image is None:
        return HttpResponse('Pillow is required to generate tickets', status=500)

    # Build ticket text
    title = booking.showtime.movie.title
    theater = booking.showtime.theater.name
    date = booking.showtime.show_date.strftime('%b %d, %Y')
    time = booking.showtime.show_time.strftime('%I:%M %p')
    seats = ', '.join(f"{it.seat.row}{it.seat.number}" for it in booking.items.all())
    total = f"{booking.total_price}"
    booking_ref = f"BOOKING-{booking.id}"

    # Image size
    w, h = 900, 420
    bg = (255, 255, 255)
    header_bg = (31, 111, 235)
    accent = (6, 214, 160)

    img = Image.new('RGB', (w, h), color=bg)
    draw = ImageDraw.Draw(img)

    # Fonts (fallback to default)
    try:
        font_bold = ImageFont.truetype('arial.ttf', 28)
        font_regular = ImageFont.truetype('arial.ttf', 18)
        font_small = ImageFont.truetype('arial.ttf', 14)
    except Exception:
        font_bold = ImageFont.load_default()
        font_regular = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Header
    draw.rectangle([(0, 0), (w, 80)], fill=header_bg)
    draw.text((24, 18), 'Cinema Pro - Ticket', fill=(255, 255, 255), font=font_bold)
    draw.text((24, 46), booking_ref, fill=(255, 255, 255), font=font_small)

    # Movie block
    draw.text((24, 110), title, fill=(31, 41, 55), font=font_bold)
    draw.text((24, 150), f"Theater: {theater}", fill=(55, 65, 81), font=font_regular)
    draw.text((24, 180), f"Date: {date}", fill=(55, 65, 81), font=font_regular)
    draw.text((24, 210), f"Time: {time}", fill=(55, 65, 81), font=font_regular)

    # Seats and price
    draw.text((24, 250), f"Seats: {seats}", fill=(31, 41, 55), font=font_regular)
    draw.text((24, 290), f"Total Paid: ₱{total}", fill=accent, font=font_bold)

    # Right side box (QR placeholder)
    box_x = w - 260
    draw.rectangle([(box_x, 110), (w - 24, 330)], outline=header_bg, width=3)
    draw.text((box_x + 14, 130), 'Ticket QR', fill=(31, 41, 55), font=font_bold)
    # draw a simple QR-like pattern
    sq_size = 16
    offset_x = box_x + 14
    offset_y = 170
    for r in range(6):
        for c in range(6):
            if (r + c) % 2 == 0:
                draw.rectangle([(offset_x + c * sq_size, offset_y + r * sq_size),
                                (offset_x + (c + 1) * sq_size - 4, offset_y + (r + 1) * sq_size - 4)],
                               fill=(31, 41, 55))

    draw.text((24, 350), 'Present this ticket at the theater entrance.', fill=(99, 102, 241), font=font_small)

    # Save to BytesIO
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="ticket-{booking.id}.png"'
    return response


class BookingHistoryView(LoginRequiredMixin, ListView):
    """View booking history"""
    model = Booking
    template_name = 'bookings/booking_history.html'
    context_object_name = 'bookings'
    paginate_by = 10
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).prefetch_related('items')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'booking_history'
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    """User dashboard"""
    template_name = 'bookings/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_bookings'] = Booking.objects.filter(
            user=self.request.user
        ).order_by('-booking_date')[:5]
        context['total_bookings'] = Booking.objects.filter(
            user=self.request.user
        ).count()
        context['total_spent'] = sum(
            float(b.total_price) for b in Booking.objects.filter(
                user=self.request.user
            )
        )
        context['page'] = 'dashboard'
        return context


@login_required(login_url='login')
def add_review(request, movie_id):
    """Add review for a movie"""
    from apps.movies.models import Movie
    movie = get_object_or_404(Movie, id=movie_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movie_detail', pk=movie_id)
    else:
        form = ReviewForm()
    # Prepare choices with star counts for template rendering (avoid template int conversion issues)
    rating_choices = []
    for val, disp in form.fields['rating'].choices:
        try:
            num = int(val)
        except Exception:
            num = 0
        rating_choices.append({'value': val, 'display': disp, 'stars': range(num)})

    context = {
        'movie': movie,
        'form': form,
        'page': 'add_review',
        'rating_choices': rating_choices,
    }
    return render(request, 'bookings/add_review.html', context)


def get_seat_availability(request, showtime_id):
    """API endpoint for getting seat availability"""
    showtime = get_object_or_404(Showtime, id=showtime_id)
    
    booked_seats = BookingItem.objects.filter(
        showtime=showtime
    ).values_list('seat_id', flat=True)
    
    available_count = Seat.objects.filter(
        theater=showtime.theater
    ).exclude(id__in=booked_seats).count()
    
    return JsonResponse({
        'available_seats': available_count,
        'booked_seats': list(booked_seats),
    })
