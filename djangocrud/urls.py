from django.contrib import admin
from django.urls import path
from tasks import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('logout/', views.signout, name='logout'),
    
    # Movie URLs
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/create/', views.create_movie, name='create_movie'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movies/<int:movie_id>/update/', views.update_movie, name='update_movie'),
    path('movies/<int:movie_id>/delete/', views.delete_movie, name='delete_movie'),
    
    # Series URLs
    path('series/', views.series_list, name='series_list'),
    path('series/create/', views.create_series, name='create_series'),
    path('series/<int:series_id>/', views.series_detail, name='series_detail'),
    path('series/<int:series_id>/update/', views.update_series, name='update_series'),
    path('series/<int:series_id>/delete/', views.delete_series, name='delete_series'),
    
    # Favorites
    path('favorites/', views.favorites, name='favorites'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)