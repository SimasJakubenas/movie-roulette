from django.urls import include, path
from allauth.account import views as auth_views
from . import views

urlpatterns = [
    path('profile/', views.profile_page, name='profile'),
    path('profile/edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/update_picture/', views.update_profile_pic, name='update_picture'),
    path('signup/country_providers/', views.load_providers, name='load_providers'),
]