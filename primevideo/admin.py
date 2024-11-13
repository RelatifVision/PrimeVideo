from django.contrib import admin
from .models import Genre, Movie, Series
from .forms import MovieForm, SeriesForm

class MovieAdmin(admin.ModelAdmin):
    form = MovieForm
    list_display = ('title', 'duration', 'created', 'director', 'get_genres')
    search_fields = ('title',)
    fields = ('title', 'description', 'image', 'director', 'genres', 'duration')

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    get_genres.short_description = 'Géneros'

class SeriesAdmin(admin.ModelAdmin):
    form = SeriesForm
    list_display = ('title', 'seasons', 'episodes', 'duration', 'created', 'director', 'get_genres')
    search_fields = ('title',)
    fields = ('title', 'description', 'image', 'director', 'genres', 'seasons', 'episodes', 'duration')

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    get_genres.short_description = 'Géneros'

admin.site.register(Genre)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Series, SeriesAdmin)