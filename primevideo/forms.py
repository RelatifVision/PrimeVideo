from django import forms
from .models import Movie, Series

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'duration', 'favorite', 'image', 'director', 'genres']
        widgets = {
            'genres': forms.CheckboxSelectMultiple(),  # Esto permite seleccionar múltiples géneros
        }

class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ['title', 'description', 'seasons', 'episodes', 'favorite', 'image', 'director', 'genres']
        widgets = {
            'genres': forms.CheckboxSelectMultiple(),  # Esto permite seleccionar múltiples géneros
        }
