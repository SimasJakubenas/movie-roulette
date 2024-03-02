import os
import requests
import random
from django.shortcuts import render, reverse, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from .forms import RouletteSourceForm
from .models import MovieOrShow, Genre, Person, Actor, Director, Creator, Country

# Create your views here.
# class TitleList(generic.ListView):
#     queryset = MovieOrShow.objects.all()

API_KEY = os.environ.get('API_KEY')
BASE_URL = 'https://api.themoviedb.org/3'
DISCOVER_MOVIE = '/discover/movie'
DISCOVER_SHOW = '/discover/tv'
ENDPOINT_POPULAR_TITLES = 'include_adult=false&language=en-US&page=1&sort_by=popularity.desc&watch_region=IE&with_watch_providers=8'
POSTER_BASE_URL = 'https://image.tmdb.org/t/p/'
POSTER_SIZE = 'w154/'
POSTER_PATH = POSTER_BASE_URL + POSTER_SIZE

def tmdb_api_connect(request, type):
    if ( type == 'Movie'):
        url = f"{BASE_URL}{DISCOVER_MOVIE}?api_key={API_KEY}&{ENDPOINT_POPULAR_TITLES}"
    else:
        url = f"{BASE_URL}{DISCOVER_SHOW}?api_key={API_KEY}&{ENDPOINT_POPULAR_TITLES}"
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
        slice_date = slice(4)
        new_entry.date = result_pick['release_date'][slice(4)]
        new_entry.save()
    else:
        new_entry.title = result_pick['name']
        new_entry.type = 1
        slice_date = slice(4)
        new_entry.date = result_pick['first_air_date'][slice(4)]
        new_entry.save()
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

def title_info(request):
    """
    Receives data from user input and uses that data to call to an API to fetch 
    detailed information about the title
    """
    if request.method == 'POST':
        titleID = request.POST.get('titleID')
        titleType = request.POST.get('titleType')
        if ( titleType == '0' ):
            url = f'{BASE_URL}/movie/{titleID}?api_key={API_KEY}&append_to_response=casts,videos,releases'
        else:
            url = f'{BASE_URL}/tv/{titleID}?api_key={API_KEY}&append_to_response=credits,videos,releases'
        headers = {
            "accept": "application/json",
        }
        response = requests.get(url, headers=headers)
        title_details = response.json()
        get_title = MovieOrShow.objects.get(title_id=titleID)
        for each_genre in title_details['genres']:
            genre, created  = Genre.objects.get_or_create(
                genre_id=each_genre['id'],
                defaults={
                    'name': each_genre['name'],
                    }
            )
            get_title.genres.add(genre)
        get_title.status = title_details['status']
        if ( titleType == '0' ):
            get_all_movie_people(title_details, get_title)
            get_title.runtime = title_details['runtime']
            get_title.age_limit = title_details['releases']['countries'][0]['certification']
            get_title.save()
        else:
            get_all_tv_people(title_details, get_title)
            get_title.seasons = title_details['last_episode_to_air']['season_number']
            get_title.save()

        return HttpResponse(response)

def get_all_movie_people(title_details, get_title):
    """
    Loops through 'cast' array in the API responce and creates new Person instances
    Limited to 5 actors per title as It was slowing down loading times significantlt
    Loops through crew array, checks for 'Director' and creates new Person instances
    """
    if len(title_details['casts']['cast']) < 5:
        for each_person in title_details['casts']['cast']:
            new_person_instance(each_person)
            new_actor_instance(each_person, get_title)
    else:
        for each_person in title_details['casts']['cast'][:5]:
            new_person_instance(each_person)
            new_actor_instance(each_person, get_title)

    for each_person in title_details['casts']['crew']:
        if each_person['job'] == 'Director':
            new_person_instance(each_person)
            director, created  = Director.objects.get_or_create(
                director_id=each_person['credit_id'],
                person_id=get_object_or_404(Person.objects.filter(pk=each_person['id']))
            )
            get_title.directors.add(director)

def get_all_tv_people(title_details, get_title):
    """
    Loops through 'cast' array in the API responce and creates new Person instances
    Limited to 5 actors per title as It was slowing down loading times significantlt
    Loops through created_by array creates new Person instances

    """
    if len(title_details['credits']['cast']) < 5:
        for each_person in title_details['credits']['cast']:
            new_person_instance(each_person)
            new_actor_instance(each_person, get_title)
    else:
        for each_person in title_details['credits']['cast'][:5]:
            new_person_instance(each_person)
            new_actor_instance(each_person, get_title)

    for each_person in title_details['created_by']:
        new_person_instance(each_person)
        creator, created  = Creator.objects.get_or_create(
            creator_id=each_person['credit_id'],
            person_id=get_object_or_404(Person.objects.filter(pk=each_person['id']))
        )
        get_title.creators.add(creator)


def new_person_instance(each_person):
    """
    Creates a new attribute in the Person entity
    """
    person, created  = Person.objects.get_or_create(
        person_id=each_person['id'],
        defaults={
            'full_name': each_person['name'],
        }
    )

def new_actor_instance(each_person, get_title):
    """
    Creates a new attribute in the Actor entity
    """
    actor, created  = Actor.objects.get_or_create(
        actor_id=each_person['credit_id'],
        person_id=get_object_or_404(Person.objects.filter(pk=each_person['id']))
    )
    get_title.actors.add(actor)
