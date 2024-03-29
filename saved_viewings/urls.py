from django.urls import path
from . import views

urlpatterns = [
    path('mylists/type/', views.load_list_type, name='list-type'),
    path('mylists/list/', views.load_selected_list, name='list'),
    path('mylists/', views.load_list, name='my_lists'),
    path('mylists/delete/<int:title_id>', views.clear_one_listed_title, name='delete_from_list'),
    path('mylists/info/', views.title_info, name='info'),
    path('mylists/add/', views.add_to_list, name='add_to_list'),
    path('mylists/remove/', views.remove_from_list, name='remove_from_list')
]