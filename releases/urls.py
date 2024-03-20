from . import views
from django.urls import path

urlpatterns = [
    path('movies/', views.movie_releases, name='movie_releases')
]