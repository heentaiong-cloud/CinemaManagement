"""
URL configuration for cinema_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse
from apps.bookings.views import RegisterView, LoginView, LogoutView, DashboardView
from apps.movies.models import Movie

# Home view
class HomeView(View):
    def get(self, request):
        featured_movies = Movie.objects.filter(status='active')[:8]
        context = {
            'featured_movies': featured_movies,
            'page': 'home',
        }
        return render(request, 'home.html', context)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('movies/', include('apps.movies.urls')),
    path('bookings/', include('apps.bookings.urls')),
    
    # Auth URLs
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

# Movie detail and search
from apps.movies.views import MovieDetailView, MovieSearchView
urlpatterns += [
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('search/', MovieSearchView.as_view(), name='movie_search'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
