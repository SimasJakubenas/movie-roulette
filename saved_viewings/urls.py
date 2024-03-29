from django.urls import path
from . import views

urlpatterns = [
    path('type/', views.load_list_type, name='list-type'),
    path('list/', views.load_selected_list, name='list'),
    path('', views.load_list, name='my_lists'),
    path('delete/<int:title_id>', views.clear_one_listed_title, name='delete_from_list'),
    path('info/', views.title_info, name='info'),
    path('add/', views.add_to_list, name='add_to_list'),
    path('remove/', views.remove_from_list, name='remove_from_list')
]