from django.urls import include, path
from . import views

urlpatterns = [
    path('account/logout/', views.logout_page, name='account_logout'),
    path('profile/', views.profile_page, name='profile'),
    path(
        'profile/delete_profile/',
        views.delete_profile,
        name='delete_profile'
    ),
    path('profile/edit_profile/', views.edit_profile, name='edit_profile'),
    path(
        'profile/update_picture/',
        views.update_profile_pic,
        name='update_picture'
    ),
    path(
        'signup/country_providers/',
        views.load_providers,
        name='load_providers'
    ),
]
