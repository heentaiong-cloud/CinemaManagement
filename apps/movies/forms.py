from django import forms
from .models import Movie, Theater, Showtime, Seat


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'genre', 'director', 'duration', 'rating', 'status', 'poster', 'release_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'director': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'poster': forms.FileInput(attrs={'class': 'form-control'}),
            'release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class TheaterForm(forms.ModelForm):
    class Meta:
        model = Theater
        fields = ['name', 'location', 'total_seats']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'total_seats': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ShowtimeForm(forms.ModelForm):
    class Meta:
        model = Showtime
        fields = ['movie', 'theater', 'show_date', 'show_time', 'ticket_price']
        widgets = {
            'movie': forms.Select(attrs={'class': 'form-control'}),
            'theater': forms.Select(attrs={'class': 'form-control'}),
            'show_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'show_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'ticket_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
