from django.contrib import admin
from .models import Movie, Series

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'created', 'favorite')
    search_fields = ('title',)

class SeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'seasons', 'episodes', 'created', 'favorite')
    search_fields = ('title',)

# Registrar los modelos
admin.site.register(Movie, MovieAdmin)
admin.site.register(Series, SeriesAdmin)
