from django import forms
from .models import Movie, Series

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'duration', 'favorite', 'image']

class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ['title', 'description', 'seasons', 'episodes', 'favorite', 'image']