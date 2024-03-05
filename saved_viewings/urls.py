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
    path('mylists/<str:list_type>/', views.load_favourites_list, name='my_lists'),
    path('mylists/<str:list_type>/delete/<int:title_id>', views.clear_one_favourite_title, name='delete_from_list'),
    path('mylists/<str:list_type>/info/', views.title_info, name='info'),
    path('mylists/<str:list_type>/add/', views.add_to_list, name='add_to_list'),
    path('mylists/<str:list_type>/remove/', views.remove_from_list, name='remove_from_list')
    
]