from . import views
from django.urls import path

urlpatterns = [
    # path('', views.TitleList.as_view(template_name="saved_viewings/roulette_list.html"), name='roulette'),
    path('', views.roulette_list, name='roulette_list'),
    path('clearall/', views.roulette_clear, name='clear_list'),
    path('delete/<int:title_id>', views.clear_one_title, name='delete')
]