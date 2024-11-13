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
    path('movies/<int:movie_id>/watched/', views.mark_as_watched_movie, name='mark_as_watched_movie'),
    path('movies/<int:movie_id>/favorite/', views.mark_as_favorite_movie, name='mark_as_favorite_movie'),
    
    path('series/', views.series_list, name='series_list'),
    path('series/create/', views.create_series, name='create_series'),
    path('series/<int:series_id>/', views.series_detail, name='series_detail'),
    path('series/<int:series_id>/update/', views.update_series, name='update_series'),
    path('series/<int:series_id>/delete/', views.delete_series, name='delete_series'),
    path('series/<int:series_id>/watched/', views.mark_as_watched_series, name='mark_as_watched_series'),
    path('series/<int:series_id>/favorite/', views.mark_as_favorite_series, name='mark_as_favorite_series'),
    
    path('genre_list/', views.genre_list, name='genre_list'),  # Ruta para la lista de géneros
    path('genre/<int:genre_id>/', views.genre_detail, name='genre_detail'),  # Nueva ruta para el detalle del género
    path('search/', views.search, name='search'), # nueva ruta para el buscador
    
    path('user_content_graph/', views.user_content_graph, name='user_content_graph'), # nueva ruta para el gráfico de contenido del usuario
    path('admin_content_graph/', views.admin_content_graph, name='admin_content_graph'), # nueva ruta para el gráfico de contenido del administrador
    
    path('favorites/', views.favorites, name='favorites'),
    path('watched/', views.watched, name='watched'),
    
    path('settings/', views.settings_view, name='settings'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/<int:user_id>/update/', views.update_user, name='update_user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('users/<int:user_id>/change_password_admin/', views.change_password_admin, name='change_password_admin'),
    path('change_password_user/', views.change_password_user, name='change_password_user'),
    path('update_profile/', views.update_profile, name='update_profile'),
]

