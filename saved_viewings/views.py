from django.shortcuts import render
from django.views import generic
from .models import MovieOrShow

# Create your views here.
class TitleList(generic.ListView):
    queryset = MovieOrShow.objects.all()
    
