from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from .models import Movie, Series, UserContentStatus, Genre
from .forms import MovieForm, SeriesForm, UserProfileForm
from django.contrib import messages
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64


# _____Funciones Home y Registro_____

# Función de Home pagina inicio
def home(request):
    genres = Genre.objects.all()
    return render(request, 'home.html', {'genres': genres})
# Función de Registro pagina registro formulario
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
# Función de Logearse pagina inicio sesion
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
# Función de Cerrar sesión pagina salir de tu sesion
@login_required
def signout(request):
    logout(request)
    return redirect('home')

# _____Funciones Administrador Usuario_____

# Función de administrar usuarios
@login_required
@user_passes_test(lambda u: u.is_staff) # usar solo por admin
def manage_users(request):
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})
# Función de crear usuario
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
# Función de actualizar usuario
@login_required
@user_passes_test(lambda u: u.is_staff)
def update_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'update_user.html', {'form': form, 'user': user})
# Función de eliminar usuario
@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('manage_users')
    return render(request, 'delete_user.html', {'user': user})
# Función de cambiar contraseña de administrador
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
# Función de cambiar contraseña de usuario, usar cliente
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
# Función de actualizar perfil, usar cliente
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


# _____Funciones Genre_____

# Función de lista de géneros
@login_required
def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'genre_list.html', {'genres': genres})
# Función de agregar géneros al contexto
@login_required
def add_genres_to_context(request):
    genres = Genre.objects.all()
    return {'genres': genres}
# Función de detalle de género
@login_required
def genre_detail(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    movies = Movie.objects.filter(genres=genre)
    series = Series.objects.filter(genres=genre)
    genres = Genre.objects.all()
    return render(request, 'genre_detail.html', {
        'genre': genre,
        'movies': movies,
        'series': series,
        'genres': genres
    })
    
# _____Funciones Movie_____

# Función de lista de movies
@login_required
def movie_list(request):
    movies = Movie.objects.all()
    watched_movies = UserContentStatus.objects.filter(user=request.user, watched=True, movie__isnull=False).values_list('movie_id', flat=True)
    favorite_movies = UserContentStatus.objects.filter(user=request.user, favorite=True, movie__isnull=False).values_list('movie_id', flat=True)
    genres = Genre.objects.all()
    return render(request, 'movie_list.html', {
        'movies': movies,
        'watched_movies': watched_movies,
        'favorite_movies': favorite_movies,
        'genres': genres
    })
# Función de crear movie
@login_required
def create_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                movie = form.save(commit=False)
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
# Función de detalle de movie
@login_required
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    user_status, created = UserContentStatus.objects.get_or_create(user=request.user, movie=movie)
    return render(request, 'movie_detail.html', {
        'movie': movie,
        'watched': user_status.watched,
        'favorite': user_status.favorite,
    })
# Función de actualizar movie
@login_required
def update_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm(instance=movie)
    return render(request, 'update_content.html', {'form': form, 'movie': movie})
# Función de eliminar movie
@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')
    return render(request, 'delete_content.html', {'content': movie})
# Función de marcar como visto movie
@login_required
def mark_as_watched_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    user_status, created = UserContentStatus.objects.get_or_create(user=request.user, movie=movie)
    user_status.watched = not user_status.watched
    user_status.save()
    return redirect('movie_detail', movie_id=movie.id)
# Función de marcar como favorito movie
@login_required
def mark_as_favorite_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    user_status, created = UserContentStatus.objects.get_or_create(user=request.user, movie=movie)
    user_status.favorite = not user_status.favorite
    user_status.save()
    return redirect('movie_detail', movie_id=movie.id)

# _____Funciones Series_____

# Función de lista de series
@login_required
def series_list(request):
    series = Series.objects.all()
    watched_series = UserContentStatus.objects.filter(user=request.user, watched=True, series__isnull=False).values_list('series_id', flat=True)
    favorite_series = UserContentStatus.objects.filter(user=request.user, favorite=True, series__isnull=False).values_list('series_id', flat=True)
    genres = Genre.objects.all()
    return render(request, 'series_list.html', {
        'series': series,
        'watched_series': watched_series,
        'favorite_series': favorite_series,
        'genres': genres
    })
# Función de crear series
@login_required
def create_series(request):
    if request.method == 'POST':
        form = SeriesForm(request.POST, request.FILES)
        if form.is_valid():
            series = form.save(commit=False)
            series.save()
            messages.success(request, 'Series created successfully!')
            return redirect('series_list')
        else:
            messages.error(request, 'Error creating series. Please correct the errors below.')
    else:
        form = SeriesForm()
    return render(request, 'create_content.html', {'form': form})
# Función de detalle de series
@login_required
def series_detail(request, series_id):
    series = get_object_or_404(Series, pk=series_id)
    user_status, created = UserContentStatus.objects.get_or_create(user=request.user, series=series)
    return render(request, 'series_detail.html', {
        'series': series,
        'watched': user_status.watched,
        'favorite': user_status.favorite,
    })
# Función de actualizar series
@login_required
def update_series(request, series_id):
    series = get_object_or_404(Series, pk=series_id)
    if request.method == 'POST':
        form = SeriesForm(request.POST, request.FILES, instance=series)
        if form.is_valid():
            form.save()
            return redirect('series_list')
    else:
        form = SeriesForm(instance=series)
    return render(request, 'update_content.html', {'form': form, 'series': series})
# Función de eliminar series
@login_required
def delete_series(request, series_id):
    series = get_object_or_404(Series, pk=series_id)
    if request.method == 'POST':
        series.delete()
        return redirect('series_list')
    return render(request, 'delete_content.html', {'content': series})
# Función de marcar como visto series
@login_required
def mark_as_watched_series(request, series_id):
    series = get_object_or_404(Series, pk=series_id)
    user_status, created = UserContentStatus.objects.get_or_create(user=request.user, series=series)
    user_status.watched = not user_status.watched
    user_status.save()
    return redirect('series_detail', series_id=series.id)
# Función de marcar como favorito series
@login_required
def mark_as_favorite_series(request, series_id):
    series = get_object_or_404(Series, pk=series_id)
    user_status, created = UserContentStatus.objects.get_or_create(user=request.user, series=series)
    user_status.favorite = not user_status.favorite
    user_status.save()
    return redirect('series_detail', series_id=series.id)

# _____Funciones Favoritos y Vistos_____

# Función de favoritos
@login_required
def favorites(request):
    favorite_movies = UserContentStatus.objects.filter(user=request.user, favorite=True, movie__isnull=False).select_related('movie')
    favorite_series = UserContentStatus.objects.filter(user=request.user, favorite=True, series__isnull=False).select_related('series')
    watched_movies = UserContentStatus.objects.filter(user=request.user, watched=True, movie__isnull=False).values_list('movie_id', flat=True)
    watched_series = UserContentStatus.objects.filter(user=request.user, watched=True, series__isnull=False).values_list('series_id', flat=True)
    genres = Genre.objects.all()
    return render(request, 'favorites.html', {
        'favorite_movies': [status.movie for status in favorite_movies],
        'favorite_series': [status.series for status in favorite_series],
        'watched_movies': watched_movies,
        'watched_series': watched_series,
        'genres': genres
    })
# Función de visto
@login_required  
def watched(request):
    watched_movies = UserContentStatus.objects.filter(user=request.user, watched=True, movie__isnull=False).select_related('movie')
    watched_series = UserContentStatus.objects.filter(user=request.user, watched=True, series__isnull=False).select_related('series')
    favorite_movies = UserContentStatus.objects.filter(user=request.user, favorite=True, movie__isnull=False).values_list('movie_id', flat=True)
    favorite_series = UserContentStatus.objects.filter(user=request.user, favorite=True, series__isnull=False).values_list('series_id', flat=True)
    genres = Genre.objects.all()
    return render(request, 'watched.html', {
        'watched_movies': [status.movie for status in watched_movies],
        'watched_series': [status.series for status in watched_series],
        'favorite_movies': favorite_movies,
        'favorite_series': favorite_series,
        'genres': genres
    })

# _____Funciones Buscador_____
# Función de buscador por 
@login_required
def search(request):
    query = request.GET.get('q')
    genres = Genre.objects.all()
    if query:
        movies = Movie.objects.filter(Q(title__icontains=query) | Q(genres__name__icontains=query)).distinct()
        series = Series.objects.filter(Q(title__icontains=query) | Q(genres__name__icontains=query)).distinct()
    else:
        movies = Movie.objects.all()
        series = Series.objects.all()
    return render(request, 'search_results.html', {
        'movies': movies,
        'series': series,
        'genres': genres,
        'query': query
    })

# _____Funciones Settings_____

# Función de vista de ajustes 
def settings_view(request):
    return render(request, 'settings.html')



#_____Funciones Graficos Usuario & Administrador_____

# Función de grafico de contenido visto por usuario
@login_required
def user_content_graph(request):
    user = request.user
    watched_movies = UserContentStatus.objects.filter(user=user, watched=True, movie__isnull=False).select_related('movie')
    watched_series = UserContentStatus.objects.filter(user=user, watched=True, series__isnull=False).select_related('series')

    movie_durations = [status.movie.duration for status in watched_movies]
    series_durations = [status.series.seasons * status.series.episodes * status.series.duration for status in watched_series]

    total_durations = movie_durations + series_durations

    plt.figure(figsize=(10, 6))
    plt.hist(total_durations, bins=20, color='blue', edgecolor='black')
    plt.title('Duración de Contenido Visto')
    plt.xlabel('Duración (minutos)')
    plt.ylabel('Cantidad de Contenidos')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return render(request, 'user_content_graph.html', {'graphic': graphic})


# Función de grafico de contenido visto por administrador
@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_content_graph(request):
    users = User.objects.all()
    user_graphics = []

    for user in users:
        watched_movies = UserContentStatus.objects.filter(user=user, watched=True, movie__isnull=False).select_related('movie')
        watched_series = UserContentStatus.objects.filter(user=user, watched=True, series__isnull=False).select_related('series')

        movie_durations = [status.movie.duration for status in watched_movies]
        series_durations = [status.series.seasons * status.series.episodes * status.series.duration for status in watched_series]

        total_durations = movie_durations + series_durations

        plt.figure(figsize=(10, 6))
        plt.hist(total_durations, bins=20, color='blue', edgecolor='black')
        plt.title(f'Duración de Contenido Visto por {user.username}')
        plt.xlabel('Duración (minutos)')
        plt.ylabel('Cantidad de Contenidos')

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')

        user_graphics.append({'username': user.username, 'graphic': graphic})

    return render(request, 'admin_content_graph.html', {'user_graphics': user_graphics})