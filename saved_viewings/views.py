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
POSTER_PATH = POSTER_BASE_URL + POSTER_SIZE


def roulette_list(request):
    loop = True
    source_form = RouletteSourceForm(data=request.POST)
    in_roulette_list = list(MovieOrShow.objects.filter(is_in_roulette=True).values())

    if request.method == "POST":
        if source_form.is_valid():
            url = f"{BASE_URL}{ENDPOINT_POPULAR_MOVIE}&api_key={API_KEY}"
            headers = {
                "accept": "application/json",
            }
            response = requests.get(url, headers=headers)
            result = response.json()['results']
            roulette_load(request, result, loop, source_form)
    in_roulette_list = list(MovieOrShow.objects.filter(is_in_roulette=True).values())     
    return render(
        request,
        'saved_viewings/roulette_list.html',
        {
            'source_form': source_form,
            'POSTER_PATH': POSTER_PATH,
            'in_roulette_list': in_roulette_list
        })

def roulette_load(request, result, loop, source_form):
    while loop:
        random_number = random.randint(1, len(result)-1)
        result_pick = result[random_number]
        in_roulette_list = list(MovieOrShow.objects.filter(is_in_roulette=True).values())
        if len(in_roulette_list) == 0:
            new_entry = MovieOrShow(
                title_id=result_pick['id'],
                user_id=request.user,
                title=result_pick['title'],
                description=result_pick['overview'],
                tmdb_rating=result_pick['vote_average'],
                type=0,
                date=result_pick['release_date'],
                poster_link=result_pick['poster_path'],
                backdrop_link=result_pick['backdrop_path'],
                is_in_roulette=True
            )
            new_entry.save()
        if len(in_roulette_list) < 5:
            for title in in_roulette_list:
                if result_pick['id'] in title:
                    pass
                else:
                    new_entry = MovieOrShow(
                        title_id=result_pick['id'],
                        user_id=request.user,
                        title=result_pick['title'],
                        description=result_pick['overview'],
                        tmdb_rating=result_pick['vote_average'],
                        type=0,
                        date=result_pick['release_date'],
                        poster_link=result_pick['poster_path'],
                        backdrop_link=result_pick['backdrop_path'],
                        is_in_roulette=True
                    )
                    new_entry.save()

        else:
            loop = False

    return in_roulette_list, render(
        request,
        'saved_viewings/roulette_list.html',
        {
            'source_form': source_form,
            'POSTER_PATH': POSTER_PATH,
            'in_roulette_list': in_roulette_list
        })
