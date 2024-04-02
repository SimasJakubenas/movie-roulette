from django.urls import path
from saved_viewings import views as list_views
from . import views

urlpatterns = [
    path('', views.search_page, name='search'),
    path('add/', list_views.add_to_list, name='add_to_list'),
    path('genres/', views.search_genres, name='genres'),
    path('info/', list_views.title_info, name='info'),
    path('remove/', list_views.remove_from_list, name='remove_from_list'),
    path('results/', views.search_results, name='search_results')
]