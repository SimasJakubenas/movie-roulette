import os
import requests
import random
import json
from django.shortcuts import render, reverse, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from roulette.forms import RouletteSourceForm
from .models import MovieOrShow, Genre, Person, Actor, Director, Creator, StreamingService
from accounts.models import Country, Profile


API_KEY = os.environ.get('API_KEY')
BASE_URL = 'https://api.themoviedb.org/3'
DISCOVER_MOVIE = '/discover/movie'
DISCOVER_SHOW = '/discover/tv'
POSTER_BASE_URL = 'https://image.tmdb.org/t/p/'
POSTER_SIZE = 'w154/'
POSTER_PATH = POSTER_BASE_URL + POSTER_SIZE


def add_title_instance(request, result, result_pick, source, type):
    """
    If roulette page form source is 'Random': creates a new instance in MovieOrShow entity
    Otherwise adds a title to roulette from database by changing it's boolean value
    """
    if source == 'Random':
        new_entry = MovieOrShow.objects.get_or_create(
            title_id=result_pick['id'],
            user_id=request.user,
            defaults={
                'description': result_pick['overview'],
                'tmdb_rating': result_pick['vote_average'],
                'poster_link': result_pick['poster_path'],
                'backdrop_link': result_pick['backdrop_path'],
                'is_in_roulette': True
            }
        )
        type = 'Movies' if type == 0 else 'TV Shows'
        get_title = MovieOrShow.objects.filter(user_id=request.user.id, title_id=result_pick['id'])
        if ( type == 'Movies'):
            update_title = get_title.update(title=result_pick['title'])
            update_title = get_title.update(type=0)
            update_title = get_title.update(date=result_pick['release_date'][slice(4)])
        else:
            update_title = get_title.update(title=result_pick['name'])
            update_title = get_title.update(type=1)
            update_title = get_title.update(date=result_pick['first_air_date'][slice(4)])
    
    else:
        get_query = MovieOrShow.objects.filter(user_id=request.user.id, title_id=result_pick['id'])
        get_query.update(is_in_roulette = True)
        for title in result:
            if title['title_id'] == result_pick['id']:
                result.remove(title)
                return result


@login_required
def clear_one_listed_title(request, title_id, list_type=None):
    """
    Queries the database for a specific title
    Removes a single title from the corresponding list
    Redirects to mylists page
    """
    if request.method == 'POST':
        get_title = MovieOrShow.objects.filter(user_id=request.user.id, title_id=title_id)

        if list_type == 'favourites':
            update_title = get_title.update(is_in_favourites=False)
        if list_type == 'watchlist':
            update_title = get_title.update(is_in_watchlist=False)
        if list_type == 'seen_it':
            update_title = get_title.update(is_in_seen_it=False)
        if list_type == 'dont_show':
            update_title = get_title.update(is_in_dont_show=False)
        clear_title(request, get_title, title_id)

        if list_type:
            return HttpResponse('Title removed from list')
        else:
            return HttpResponseRedirect(reverse('my_lists', args=[list_type]))

    return HttpResponseRedirect(reverse('my_lists', args=[title_id]))


def clear_title(request, get_title, title_id):
    """
    Queries the database for a specific title
    If title is in database and not in any of the lists - deletes the title
    """
    title_object = list(MovieOrShow.objects.filter(user_id=request.user.id, title_id=title_id).values())

    if len(title_object) > 0:
        if (title_object[0]['is_in_roulette'] or 
            title_object[0]['is_in_favourites'] or
            title_object[0]['is_in_watchlist'] or
            title_object[0]['is_in_seen_it'] or
            title_object[0]['is_in_dont_show'] or
            title_object[0]['is_in_roulette']
            in title_object) == True:
            pass
        else:
            get_title.delete()
    else:
        pass


@login_required
def title_info(request, list_type=None):
    """
    Receives data from user input and uses that data to call to an API to fetch 
    detailed information about the title
    Pulls MovieOrShow instance from database/ creates new instance
    Appends this data to API response and passes all colective data back to async function
    """
    if request.method == 'POST':
        titleID = request.POST.get('titleID')
        titleType = request.POST.get('titleType')
        if ( titleType == '0' ):
            url = f'{BASE_URL}/movie/{titleID}?api_key={API_KEY}&append_to_response=casts,videos,releases'
            stream_url = f'{BASE_URL}/movie/{titleID}/watch/providers?api_key={API_KEY}'
        else:
            url = f'{BASE_URL}/tv/{titleID}?api_key={API_KEY}&append_to_response=credits,videos,releases'
            stream_url = f'{BASE_URL}/tv/{titleID}/watch/providers?api_key={API_KEY}'
        headers = {
            "accept": "application/json",
        }
        response = requests.get(url, headers=headers)
        title_details = response.json()

        stream_response = requests.get(stream_url, headers=headers)
        available_stream_details = stream_response.json()
        title_details.update(available_stream_details)
        get_title = MovieOrShow.objects.get_or_create(
            title_id=title_details['id'],
            user_id=request.user,
            defaults={
                'description': title_details['overview'],
                'tmdb_rating': title_details['vote_average'],
                'poster_link': title_details['poster_path'],
                'backdrop_link': title_details['backdrop_path'],
            }
        )
        get_title = MovieOrShow.objects.filter(user_id=request.user.id, title_id=titleID)
        if ( titleType == '0'):
            update_title = get_title.update(title=title_details['title'])
            update_title = get_title.update(type=0)
            update_title = get_title.update(date=title_details['release_date'][slice(4)])
        else:
            update_title = get_title.update(title = title_details['name'])
            update_title = get_title.update(type=1)
            update_title = get_title.update(date=title_details['first_air_date'][slice(4)])
        
        for each_genre in title_details['genres']:
            genre, created  = Genre.objects.get_or_create(
                genre_id=each_genre['id'],
                defaults={
                    'name': each_genre['name'],
                    }
            )
            get_title[0].genres.add(genre)

        get_title_providers(request, titleType, titleID, get_title, available_stream_details)
       
        get_title.update(status=title_details['status'])
        if ( titleType == '0' ):
            get_all_movie_people(title_details, get_title)
            get_title.update(runtime = title_details['runtime'])
            get_title.update(age_limit = title_details['releases']['countries'][0]['certification'])
        else:
            get_all_tv_people(title_details, get_title)
            get_title.update(seasons = title_details['last_episode_to_air']['season_number'])
        
        get_title = list(MovieOrShow.objects.filter(user_id=request.user.id, title_id=titleID).values())
        del get_title[0]['uuid']
        title_details.update(get_title[0])

        get_profile = Profile.objects.get(user_id=request.user.id)
        get_country = Country.objects.get(name=get_profile.country)
        get_profile_streams = list(get_profile.streams.all().values())
        title_providers = {}
        title_providers['provider_name'] = []
        for profile_stream in get_profile_streams:
            title_providers['provider_name'].append((profile_stream['name']))
        country_id = {}
        country_id['user_country'] = get_country.country_iso
        title_details.update(country_id)
        title_details.update(title_providers)
        myResponse = json.dumps(title_details)

        return HttpResponse(myResponse)


@login_required
def add_to_list(request, list_type=None):
    """
    Receives data from list icon toggle and uses that data to add title
    to respective list 
    """
    if request.method == 'POST':
        titleID = request.POST.get('titleID')
        list = request.POST.get('list')
        if list == 'favourites':
            get_title = MovieOrShow.objects.filter(
                user_id=request.user.id, title_id=titleID).update(is_in_favourites=True
            )
        if list == 'watchlist':
            get_title = MovieOrShow.objects.filter(
                user_id=request.user.id, title_id=titleID).update(is_in_watchlist=True
            )
        if list == 'seen_it':
            get_title = MovieOrShow.objects.filter(
                user_id=request.user.id, title_id=titleID).update(is_in_seen_it=True
            )
        if list == 'dont_show':
            get_title = MovieOrShow.objects.filter(
                user_id=request.user.id, title_id=titleID).update(is_in_dont_show=True
            )

        return HttpResponse('add to list')


@login_required
def remove_from_list(request):
    """
    Receives data from list icon toggle and uses that data to remove title
    from respective list
    """
    if request.method == 'POST':
        title_id = request.POST.get('titleID')
        list_type = request.POST.get('list')

        if list_type == 'roulette':
            get_title = MovieOrShow.objects.filter(
                user_id=request.user.id, title_id=title_id
            )
            print(get_title)
            update_title = get_title.update(is_in_favourites=False)
        if list_type == 'favourites':
            get_title = MovieOrShow.objects.filter(
                user_id=request.user.id, title_id=title_id
            )
            update_title = get_title.update(is_in_favourites=False)
        if list_type == 'watchlist':
            get_title = MovieOrShow.objects.filter(
                user_id=request.user.id, title_id=title_id
            )
            update_title = get_title.update(is_in_watchlist=False)
        if list_type == 'seen_it':
            get_title = MovieOrShow.objects.filter(
                user_id=request.user.id, title_id=title_id
            )
            update_title = get_title.update(is_in_seen_it=False)
        if list_type == 'dont_show':
            get_title = MovieOrShow.objects.filter(
                user_id=request.user.id, title_id=title_id
            )
            update_title = get_title.update(is_in_dont_show=False)
        clear_title(request, get_title, title_id)

        return HttpResponse('Removed from list')


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
            get_title[0].directors.add(director)


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
        get_title[0].creators.add(creator)


def get_title_providers(request, titleType, titleID, get_title, available_stream_details):
    """
    Connects to an API end point for streaming providers
    Loops through different areas of the response and updates StreamingServices model

    """
    get_profile = Profile.objects.get(user_id=request.user.id)
    get_country = Country.objects.get(name=get_profile.country)
    if get_country.country_iso in available_stream_details['results']:
        if 'flatrate' in available_stream_details['results'][get_country.country_iso]:
            for each_stream in available_stream_details['results'][get_country.country_iso]['flatrate']:
                stream_instance(each_stream, get_title)
        if 'rent' in available_stream_details['results'][get_country.country_iso]:
            for each_stream in available_stream_details['results'][get_country.country_iso]['rent']:
                stream_instance(each_stream, get_title)

        if 'buy' in available_stream_details['results'][get_country.country_iso]:
            for each_stream in available_stream_details['results'][get_country.country_iso]['buy']:
                stream_instance(each_stream, get_title)


def stream_instance(each_stream, get_title):
    """
    Creates a new streaming provider instance in the Person StreamingService
    """
    stream, created  = StreamingService.objects.get_or_create(
    provider_id=each_stream['provider_id'],
    defaults={
        'name': each_stream['provider_name'],
        'logo_path': each_stream['logo_path']
        }
    )
    get_title[0].streaming_services.add(stream)


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
    get_title[0].actors.add(actor)


@login_required
def load_list(request, list_type=None):
    """
    Gathers data from roulette form/ django user model/ profile model
    Get listed values of MovieOrShow entitry for specific instances
    Renders corresponding pade and passes all the data
    **Context**

    `source_form`
        Data from roulettes restriction fields
    `in_list`
        List of title instances in the fsvourites list

    **Templates**

    'saved_viewings/favourites.html`
    'saved_viewings/watchlist.html'
    'saved_viewings/seen_it.html'
    'saved_viewings/dont_show.html'
    """
    source_form = RouletteSourceForm(data=request.POST)
    user_data = User.objects.get(pk=request.user.id)
    profile_data = Profile.objects.get(user_id=request.user.id)

    in_list = list(MovieOrShow.objects.filter(
        user_id=request.user.id, is_in_favourites=True, type=1).values()
    )
    return render(
        request,
        'saved_viewings/lists_initial.html',
        {
            'source_form': source_form,
            "profile_data": profile_data,
            "user_data": user_data,
            'POSTER_PATH': POSTER_PATH,
            'in_list': in_list
        }
    )

    if list_type == 'favourites':
        return render(
            request,
            'saved_viewings/favourites.html',
            {
                'source_form': source_form,
                "profile_data": profile_data,
                "user_data": user_data,
                'POSTER_PATH': POSTER_PATH,
                'in_list': in_list
            }
        )

    if list_type == 'watchlist':
        in_list = list(MovieOrShow.objects.filter(
            user_id=request.user.id, is_in_watchlist=True).values()
        )

        return render(
            request,
            'saved_viewings/watchlist.html',
            {
                'source_form': source_form,
                "profile_data": profile_data,
                "user_data": user_data,
                'POSTER_PATH': POSTER_PATH,
                'in_list': in_list
            }
        )

    if list_type == 'seen_it':
        in_list = list(MovieOrShow.objects.filter(
            user_id=request.user.id, is_in_seen_it=True).values()
        )

        return render(
            request,
            'saved_viewings/seen_it.html',
            {
                'source_form': source_form,
                "profile_data": profile_data,
                "user_data": user_data,
                'POSTER_PATH': POSTER_PATH,
                'in_list': in_list
            }
        )

    if list_type == 'dont_show':
        in_list = list(MovieOrShow.objects.filter(
            user_id=request.user.id, is_in_dont_show=True).values()
            )

        return render(
            request,
            'saved_viewings/dont_show.html',
            {
                'source_form': source_form,
                "profile_data": profile_data,
                "user_data": user_data,
                'POSTER_PATH': POSTER_PATH,
                'in_list': in_list
            }
        )


@login_required
def load_selected_list(request):
    type = request.GET.get('type')
    selected_list = request.GET.get('list')
    if type == 'Movies':
        type = 0
    else:
        type = 1

    if selected_list == 'favourites':
        in_list = list(MovieOrShow.objects.filter(
            user_id=request.user.id, type=type, is_in_favourites=True).values()
        )
    if selected_list == 'watchlist':
        in_list = list(MovieOrShow.objects.filter(
            user_id=request.user.id, type=type, is_in_watchlist=True).values()
        )
    if selected_list == 'seen_it':
        in_list = list(MovieOrShow.objects.filter(
            user_id=request.user.id, type=type, is_in_seen_it=True).values()
        )
    if selected_list == 'dont_show':
        in_list = list(MovieOrShow.objects.filter(
            user_id=request.user.id, type=type, is_in_dont_show=True).values()
        )

    source_form = RouletteSourceForm(data=request.POST)
    user_data = User.objects.get(pk=request.user.id)
    profile_data = Profile.objects.get(user_id=request.user.id)

    return render(
        request,
        'saved_viewings/favourites.html',
        {
            'source_form': source_form,
            "profile_data": profile_data,
            "user_data": user_data,
            'POSTER_PATH': POSTER_PATH,
            'in_list': in_list
        }
    )


@login_required
def load_list_type(request):
    type = request.GET.get('type')
    selected_list = request.GET.get('list')

    if type == 'Movies':
        type = 0
    
    else:
        type = 1

    if selected_list == 'favourites':
        in_list = list(MovieOrShow.objects.filter(
            user_id=request.user.id, type=type, is_in_favourites=True).values()
        )
    if selected_list == 'watchlist':
        in_list = list(MovieOrShow.objects.filter(
            user_id=request.user.id, type=type, is_in_watchlist=True).values()
        )
    if selected_list == 'seen_it':
        in_list = list(MovieOrShow.objects.filter(
            user_id=request.user.id, type=type, is_in_seen_it=True).values()
        )
    if selected_list == 'dont_show':
        in_list = list(MovieOrShow.objects.filter(
            user_id=request.user.id, type=type, is_in_dont_show=True).values()
        )

    source_form = RouletteSourceForm(data=request.POST)
    user_data = User.objects.get(pk=request.user.id)
    profile_data = Profile.objects.get(user_id=request.user.id)

    return render(
        request,
        'saved_viewings/favourites.html',
        {
            'source_form': source_form,
            "profile_data": profile_data,
            "user_data": user_data,
            'POSTER_PATH': POSTER_PATH,
            'in_list': in_list
        }
    )