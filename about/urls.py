from . import views
from django.urls import path

urlpatterns = [
    path('', views.about_movie_roulette, name='about'),
]