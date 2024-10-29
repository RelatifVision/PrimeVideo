from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/create/', views.create_movie, name='create_movie'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movies/<int:movie_id>/update/', views.update_movie, name='update_movie'),
    path('movies/<int:movie_id>/delete/', views.delete_movie, name='delete_movie'),
    path('series/', views.series_list, name='series_list'),
    path('series/create/', views.create_series, name='create_series'),
    path('series/<int:series_id>/', views.series_detail, name='series_detail'),
    path('series/<int:series_id>/update/', views.update_series, name='update_series'),
    path('series/<int:series_id>/delete/', views.delete_series, name='delete_series'),
    path('favorites/', views.favorites, name='favorites'),
    path('settings/', views.settings_view, name='settings'),
]