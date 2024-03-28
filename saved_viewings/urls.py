from django.urls import path
from . import views

urlpatterns = [
    path('mylists/<str:list_type>/', views.load_list, name='my_lists'),
    path('mylists/<str:list_type>/delete/<int:title_id>', views.clear_one_listed_title, name='delete_from_list'),
    path('mylists/<str:list_type>/info/', views.title_info, name='info'),
    path('mylists/<str:list_type>/add/', views.add_to_list, name='add_to_list'),
    path('mylists/<str:list_type>/remove/', views.remove_from_list, name='remove_from_list')
]