from . import views
from django.urls import path

urlpatterns = [
    path('', views.TitleList.as_view(template_name="saved_viewings/roulette_list.html"), name='roulette'),
]