from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_page, name='search'),
    path('genres/', views.search_genres, name='genres'),
    path('results/', views.search_results, name='search_results')
]