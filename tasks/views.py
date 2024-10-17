from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Movie, Series
from .forms import MovieForm, SeriesForm

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('movie_list')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                    'error': 'Username already exists'
                })
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm(),
                'error': 'Passwords did not match'
            })

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm(),
                'error': 'Username and password did not match'
            })
        else:
            login(request, user)
            return redirect('movie_list')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

@login_required
def movie_list(request):
    movies = Movie.objects.filter(user=request.user)
    return render(request, 'movie_list.html', {'movies': movies})

@login_required
def series_list(request):
    series = Series.objects.filter(user=request.user)
    return render(request, 'series_list.html', {'series': series})

@login_required
def create_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.save()
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'create_movie.html', {'form': form})

@login_required
def create_series(request):
    if request.method == 'POST':
        form = SeriesForm(request.POST)
        if form.is_valid():
            series = form.save(commit=False)
            series.user = request.user
            series.save()
            return redirect('series_list')
    else:
        form = SeriesForm()
    return render(request, 'create_series.html', {'form': form})

@login_required
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id, user=request.user)
    return render(request, 'movie_detail.html', {'movie': movie})

@login_required
def series_detail(request, series_id):
    series = get_object_or_404(Series, pk=series_id, user=request.user)
    return render(request, 'series_detail.html', {'series': series})

@login_required
def update_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id, user=request.user)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm(instance=movie)
    return render(request, 'update_movie.html', {'form': form, 'movie': movie})

@login_required
def update_series(request, series_id):
    series = get_object_or_404(Series, pk=series_id, user=request.user)
    if request.method == 'POST':
        form = SeriesForm(request.POST, instance=series)
        if form.is_valid():
            form.save()
            return redirect('series_list')
    else:
        form = SeriesForm(instance=series)
    return render(request, 'update_series.html', {'form': form, 'series': series})

@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id, user=request.user)
    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')
    return render(request, 'delete_movie.html', {'movie': movie})

@login_required
def delete_series(request, series_id):
    series = get_object_or_404(Series, pk=series_id, user=request.user)
    if request.method == 'POST':
        series.delete()
        return redirect('series_list')
    return render(request, 'delete_series.html', {'series': series})

@login_required
def favorites(request):
    favorite_movies = Movie.objects.filter(user=request.user, favorite=True)
    favorite_series = Series.objects.filter(user=request.user, favorite=True)
    return render(request, 'favorites.html', {
        'favorite_movies': favorite_movies,
        'favorite_series': favorite_series
    })