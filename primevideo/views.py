from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Movie, Series, WatchedContent
from .forms import MovieForm, SeriesForm, UserProfileForm, AdminProfileForm
from django.contrib import messages

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
    movies = Movie.objects.all()  # Obtener todas las películas
    watched_movies = Movie.objects.filter(user=request.user, watched=True).values_list('id', flat=True)
    favorite_movies = Movie.objects.filter(user=request.user, favorite=True).values_list('id', flat=True)
    return render(request, 'movie_list.html', {
        'movies': movies,
        'watched_movies': watched_movies,
        'favorite_movies': favorite_movies
    })

@login_required
def series_list(request):
    series = Series.objects.all()  # Obtener todas las series
    watched_series = Series.objects.filter(user=request.user, watched=True).values_list('id', flat=True)
    favorite_series = Series.objects.filter(user=request.user, favorite=True).values_list('id', flat=True)
    return render(request, 'series_list.html', {
        'series': series,
        'watched_series': watched_series,
        'favorite_series': favorite_series
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def manage_users(request):
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})

@login_required
@user_passes_test(lambda u: u.is_staff)
def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = UserCreationForm()
    return render(request, 'create_user.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def update_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = AdminProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = AdminProfileForm(instance=user)
    return render(request, 'update_user.html', {'form': form, 'user': user})

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('manage_users')
    return render(request, 'delete_user.html', {'user': user})

@login_required
@user_passes_test(lambda u: u.is_staff)
def change_password_admin(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = SetPasswordForm(user)
    return render(request, 'change_password_admin.html', {'form': form, 'user': user})

@login_required
def change_password_user(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password_user.html', {'form': form})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})

@login_required
def create_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                movie = form.save(commit=False)
                movie.user = request.user
                movie.save()
                messages.success(request, 'Movie created successfully!')
                return redirect('movie_list')
            except Exception as e:
                messages.error(request, f'Error creating movie: {e}')
        else:
            messages.error(request, 'Error creating movie. Please correct the errors below.')
    else:
        form = MovieForm()
    return render(request, 'create_content.html', {'form': form})

@login_required
def create_series(request):
    if request.method == 'POST':
        form = SeriesForm(request.POST, request.FILES)
        if form.is_valid():
            series = form.save(commit=False)
            series.user = request.user
            series.save()
            messages.success(request, 'Series created successfully!')
            return redirect('series_list')
        else:
            messages.error(request, 'Error creating series. Please correct the errors below.')
    else:
        form = SeriesForm()
    return render(request, 'create_content.html', {'form': form})

@login_required
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    watched = movie.watched if request.user.is_authenticated else False
    favorite = movie.favorite if request.user.is_authenticated else False
    return render(request, 'movie_detail.html', {
        'movie': movie,
        'watched': watched,
        'favorite': favorite,
    })

@login_required
def series_detail(request, series_id):
    series = get_object_or_404(Series, pk=series_id, user=request.user)
    watched = series.watched if request.user.is_authenticated else False
    favorite = series.favorite if request.user.is_authenticated else False
    return render(request, 'series_detail.html', {
        'series': series,
        'watched': watched,
        'favorite': favorite,
    })

@login_required
def update_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id, user=request.user)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm(instance=movie)
    return render(request, 'update_content.html', {'form': form, 'movie': movie})

@login_required
def update_series(request, series_id):
    series = get_object_or_404(Series, pk=series_id, user=request.user)
    if request.method == 'POST':
        form = SeriesForm(request.POST, request.FILES, instance=series)
        if form.is_valid():
            form.save()
            return redirect('series_list')
    else:
        form = SeriesForm(instance=series)
    return render(request, 'update_content.html', {'form': form, 'series': series})

@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id, user=request.user)
    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')
    return render(request, 'delete_content.html', {'content': movie})

@login_required
def delete_series(request, series_id):
    series = get_object_or_404(Series, pk=series_id, user=request.user)
    if request.method == 'POST':
        series.delete()
        return redirect('series_list')
    return render(request, 'delete_content.html', {'content': series})

@login_required
def mark_as_watched_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    movie.watched = not movie.watched  # Alternar el estado de visto
    movie.save()
    return redirect('movie_detail', movie_id=movie.id)

@login_required
def mark_as_favorite_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    movie.favorite = not movie.favorite  # Alternar el estado de favorito
    movie.save()
    return redirect('movie_detail', movie_id=movie.id)

@login_required
def mark_as_watched_series(request, series_id):
    series = get_object_or_404(Series, pk=series_id)
    series.watched = not series.watched  # Alternar el estado de visto
    series.save()
    return redirect('series_detail', series_id=series.id)

@login_required
def mark_as_favorite_series(request, series_id):
    series = get_object_or_404(Series, pk=series_id)
    series.favorite = not series.favorite  # Alternar el estado de favorito
    series.save()
    return redirect('series_detail', series_id=series.id)

@login_required
def favorites(request):
    favorite_movies = Movie.objects.filter(user=request.user, favorite=True)  # Obtener todas las películas favoritas del usuario
    favorite_series = Series.objects.filter(user=request.user, favorite=True)  # Obtener todas las series favoritas del usuario
    return render(request, 'favorites.html', {
        'favorite_movies': favorite_movies,
        'favorite_series': favorite_series
    })

@login_required
def watched(request):
    watched_movies = Movie.objects.filter(user=request.user, watched=True)  # Obtener todas las películas vistas del usuario
    watched_series = Series.objects.filter(user=request.user, watched=True)  # Obtener todas las series vistas del usuario
    return render(request, 'watched.html', {
        'watched_movies': watched_movies,
        'watched_series': watched_series
    })

def settings_view(request):
    return render(request, 'settings.html')