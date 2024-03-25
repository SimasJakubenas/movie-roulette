from django.urls import path
from saved_viewings.views import title_info
from . import views

urlpatterns = [
    path('movies/', views.movie_releases, name='movie_releases'),
    path('movies/info/', title_info, name='movie_info'),
    path('shows/', views.show_releases, name='show_releases'),
    path('shows/info/', title_info, name='show_info')
]