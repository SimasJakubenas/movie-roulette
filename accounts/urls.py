from django.urls import include, path
from allauth.account import views as auth_views
from . import views

urlpatterns = [
    path('signup/country_providers/', views.load_providers, name='load_providers'),
]