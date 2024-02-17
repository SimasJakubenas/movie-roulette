import os
import requests
import random
from django.shortcuts import render, reverse, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from .forms import RouletteSourceForm
from .models import MovieOrShow

# Create your views here.
# class TitleList(generic.ListView):
#     queryset = MovieOrShow.objects.all()

API_KEY = os.environ.get('API_KEY')
BASE_URL = 'https://api.themoviedb.org/3'
ENDPOINT_POPULAR_MOVIE = '/movie/popular?language=en-US&page=1'
ENDPOINT_POPULAR_SHOW = '/tv/popular?language=en-US&page=1'
POSTER_BASE_URL = 'https://image.tmdb.org/t/p/'
POSTER_SIZE = 'w154/'
POSTER_PATH = POSTER_BASE_URL + POSTER_SIZE

def tmdb_api_connect(request, type):
    if ( type == 'Movie'):
        url = f"{BASE_URL}{ENDPOINT_POPULAR_MOVIE}&api_key={API_KEY}"
    else:
        url = f"{BASE_URL}{ENDPOINT_POPULAR_SHOW}&api_key={API_KEY}"
    headers = {
        "accept": "application/json",
    }
    response = requests.get(url, headers=headers)
    result = response.json()['results']

    return result

def roulette_list(request):
    """
    Main view that controls loadind the roulette
    **Context**

    ``source_form``
        Instance of roulette restriction fields
    ``POSTER_PATH``
        URL path for posters
    ``in_roulette_list``
        List of title instances in the roullete

    **Template**
        
    :saved_viewings/roulette_list.html`
    """
    source_form = RouletteSourceForm(data=request.POST)
    in_roulette_list = list(MovieOrShow.objects.filter(is_in_roulette=True).values())

    if request.method == "POST":
        if source_form.is_valid():
            source = source_form.cleaned_data["source"]
            type = source_form.cleaned_data["type"]
            load_all = source_form.cleaned_data["load_all"]
            if (source == 'Random'):
                result = tmdb_api_connect(request, type)
            elif (source =='Favourites'):
                result = list(MovieOrShow.objects.filter(is_in_favourites=True).values()) 
            elif (source =='Watchlist'):
                result = list(MovieOrShow.objects.filter(is_in_watchlist=True).values()) 
            else:
                result = list(MovieOrShow.objects.filter(is_in_seen_it=True).values()) 
            roulette_load(request, result, source_form, source, type, load_all)
        
            
    in_roulette_list = list(MovieOrShow.objects.filter(is_in_roulette=True).values())     
    return render(
        request,
        'saved_viewings/roulette_list.html',
        {
            'source_form': source_form,
            'POSTER_PATH': POSTER_PATH,
            'in_roulette_list': in_roulette_list
        })

def roulette_load(request, result, source_form, source, type, load_all):
    """
    Loads MovieOrShow entity with titles if there's less that 5 titles in the roulette
    Uses source_form boolean field to determine weather to load all roulette items
    or just one.
    **Context**

    ``source_form``
        Instance of roulette restriction fields
    ``POSTER_PATH``
        URL path for posters
    ``in_roulette_list``
        List of title instances in the roullete

    **Template**
        
    :saved_viewings/roulette_list.html`
    """
    while True:
        if (len(result) > 0):
            if ( source == 'Random'):
                random_number = random.randint(1, len(result)-1)
            else:
                random_number = random.randint(1, len(result))
            result_pick = result[random_number]
            in_roulette_list = list(MovieOrShow.objects.filter(is_in_roulette=True).values())
            if (load_all == True):
                if len(in_roulette_list) == 0:
                    add_title_instance(request, result_pick, source, type)
                if len(in_roulette_list) < 5:
                    for title in in_roulette_list:
                        if result_pick['id'] in title:
                            pass
                        else:
                            add_title_instance(request, result_pick, source, type)
                else:
                    return False
            else:
                add_title_instance(request, result_pick, source, type)
                return False
        else:
            return False

    return in_roulette_list, render(
        request,
        'saved_viewings/roulette_list.html',
        {
            'source_form': source_form,
            'POSTER_PATH': POSTER_PATH,
            'in_roulette_list': in_roulette_list
        })

def roulette_clear(request):
    """
    View to empty roulette content
    """
    if request.method == 'POST':
        clear_list = MovieOrShow.objects.filter(is_in_roulette=True).delete()
        return HttpResponseRedirect(reverse('roulette_list'))

    return HttpResponseRedirect(reverse('roulette_list'))

def add_title_instance(request, result_pick, source, type):
    """
    Addan instanceto the MovieOrShow entity
    """
    new_entry = MovieOrShow(
        title_id=result_pick['id'],
        user_id=request.user,
        description=result_pick['overview'],
        tmdb_rating=result_pick['vote_average'],
        poster_link=result_pick['poster_path'],
        backdrop_link=result_pick['backdrop_path'],
        is_in_roulette=True
    )
    if ( type == 'Movie'):
        new_entry.title=  result_pick['title']
        new_entry.type = 0
        new_entry.date = result_pick['release_date']
    else:
        new_entry.title = result_pick['name']
        new_entry.type = 1
        new_entry.date = result_pick['first_air_date']
    new_entry.save()

def clear_one_title(request, title_id):
    """
    Removes a single title to the  roulette carousel
    """
    if request.method == 'POST':
        queryset = MovieOrShow.objects.filter(is_in_roulette=True)
        one_clicked = get_object_or_404(queryset, pk=title_id)
        one_clicked.delete()
        return HttpResponseRedirect(reverse('roulette_list'))

    return HttpResponseRedirect(reverse('roulette_list', args=[title_id]))

