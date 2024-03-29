from django.urls import path
from saved_viewings import views as list_views
from . import views

urlpatterns = [
    path('roulette', views.roulette_list, name='roulette_list'),
    path('roulette', views.roulette_list, name='add_title'),
    path('add/', list_views.add_to_list, name='add'),
    path('remove/', list_views.remove_from_list, name='remove'),
    path('clearall/', views.roulette_clear, name='clear_list'),
    path('delete/<int:title_id>', views.clear_one_title, name='delete'),
    path('info/', list_views.title_info, name='info'),
]