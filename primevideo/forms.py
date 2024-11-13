from django import forms
from .models import Movie, Series
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'duration', 'image', 'director', 'genres']
        widgets = {
            'genres': forms.CheckboxSelectMultiple(),  # Esto permite seleccionar múltiples géneros
        }

class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ['title', 'description', 'seasons', 'episodes', 'image', 'director', 'genres']
        widgets = {
            'genres': forms.CheckboxSelectMultiple(),  # Esto permite seleccionar múltiples géneros
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']