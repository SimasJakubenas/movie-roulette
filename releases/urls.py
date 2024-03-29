from django.urls import path
from saved_viewings.views import title_info, add_to_list, remove_from_list
from . import views

urlpatterns = [
    path('movies/', views.movie_releases, name='movie_releases'),
    path('movies/add/', add_to_list, name='add'),
    path('movies/info/', title_info, name='movie_info'),
    path('movies/remove/', remove_from_list, name='remove'),
    path('shows/', views.show_releases, name='show_releases'),
    path('shows/add/', add_to_list, name='add'),
    path('shows/info/', title_info, name='show_info'),
    path('shows/remove/', remove_from_list, name='remove')
]