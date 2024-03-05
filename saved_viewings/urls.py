from . import views
from django.urls import path

urlpatterns = [
    path('', views.roulette_list, name='roulette_list'),
    path('', views.roulette_list, name='add_title'),
    path('add/', views.add_to_list, name='add'),
    path('remove/', views.remove_from_list, name='remove'),
    path('clearall/', views.roulette_clear, name='clear_list'),
    path('delete/<int:title_id>', views.clear_one_title, name='delete'),
    path('info/', views.title_info, name='info'),
    path('favourite/', views.load_favourites_list, name='favourite_list'),
    path('favourite/delete/<int:title_id>', views.clear_one_favourite_title, name='delete_favourite'),
    path('favourite/info/', views.title_info, name='info'),
    path('favourite/add/', views.add_to_list, name='add_to_favourites'),
    path('favourite/remove/', views.remove_from_list, name='remove_from_favourites')
    
]