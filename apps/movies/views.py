from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Movie, Showtime
from datetime import datetime, timedelta


class MovieListView(ListView):
    """View for listing all movies"""
    model = Movie
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Movie.objects.filter(status='active')
        genre = self.request.GET.get('genre')
        if genre:
            queryset = queryset.filter(genre=genre)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Movie.objects.values_list('genre', flat=True).distinct()
        return context


class MovieDetailView(DetailView):
    """View for movie details and showtimes"""
    model = Movie
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'
    slug_field = 'id'
    slug_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get showtimes for the next 30 days
        future_date = datetime.now() + timedelta(days=30)
        context['showtimes'] = Showtime.objects.filter(
            movie=self.object,
            show_date__gte=datetime.now().date(),
            show_date__lte=future_date.date()
        ).order_by('show_date', 'show_time')
        return context


class MovieSearchView(View):
    """View for searching movies"""
    def get(self, request):
        query = request.GET.get('q', '')
        movies = Movie.objects.filter(status='active')
        
        if query:
            movies = movies.filter(
                title__icontains=query
            ) | movies.filter(
                description__icontains=query
            )
        
        context = {
            'movies': movies,
            'query': query,
        }
        return render(request, 'movies/movie_list.html', context)
