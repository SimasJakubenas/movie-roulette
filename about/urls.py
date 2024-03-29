from . import views
from django.urls import path

urlpatterns = [
    path('about/', views.about_movie_roulette, name='about'),
    path('', views.index, name='home'),
]