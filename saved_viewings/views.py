import os
import requests
import random
from django.shortcuts import render
from django.views import generic
from .forms import RouletteSourceForm
from .models import MovieOrShow

# Create your views here.
# class TitleList(generic.ListView):
#     queryset = MovieOrShow.objects.all()

API_KEY = os.environ.get('API_KEY')
BASE_URL = 'https://api.themoviedb.org/3'
ENDPOINT_POPULAR_MOVIE = '/movie/popular?language=en-US&page=1'
POSTER_BASE_URL = 'https://image.tmdb.org/t/p/'
POSTER_SIZE = 'w154/'

def roulette_list(request):
    source_form = RouletteSourceForm(data=request.POST)
    if request.method == "POST":
        if source_form.is_valid():
            url = f"{BASE_URL}{ENDPOINT_POPULAR_MOVIE}&api_key={API_KEY}"
            headers = {
                "accept": "application/json",
            }
            response = requests.get(url, headers=headers)
            result = response.json()['results']

            poster_img = POSTER_BASE_URL + POSTER_SIZE + result_pick['poster_path']

            return render(
                request,
                'saved_viewings/roulette_list.html',
                {
                    'source_form': source_form,
                    'poster_img': poster_img
                })

    return render(request, 'saved_viewings/roulette_list.html', {'source_form': source_form})

