from django.contrib import admin
from .models import Genre, Movie, Series
from .forms import MovieForm, SeriesForm

class MovieAdmin(admin.ModelAdmin):
    form = MovieForm
    list_display = ('title', 'duration', 'created', 'favorite', 'director', 'get_genres')  # Añadido director y géneros
    search_fields = ('title',)

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])  # Muestra los géneros como una cadena
    get_genres.short_description = 'Géneros'  # Título de la columna

class SeriesAdmin(admin.ModelAdmin):
    form = SeriesForm
    list_display = ('title', 'seasons', 'episodes', 'created', 'favorite', 'director', 'get_genres')  # Añadido director y géneros
    search_fields = ('title',)

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])  # Muestra los géneros como una cadena
    get_genres.short_description = 'Géneros'  # Título de la columna

admin.site.register(Genre)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Series, SeriesAdmin)
