from django.urls import include, path
from allauth.account import views as auth_views
from . import views

urlpatterns = [
    path('accounts/signup/', auth_views.SignupView.as_view(), name='sign_up'),
    path('accounts/signup/country_providers/', views.load_providers, name='load_providers'),
]