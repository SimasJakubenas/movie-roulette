import random
import requests
from django.shortcuts import render, reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from saved_viewings.models import MovieOrShow
from saved_viewings.views import (
    add_title_instance,
    clear_title,
    title_info,
    POSTER_PATH,
    BASE_URL,
    DISCOVER_SHOW,
    DISCOVER_MOVIE,
    API_KEY
)
from accounts.models import Country, Profile
from .forms import RouletteSourceForm


def tmdb_api_connect(request, type):
    """
    Connects to API and get movie/show data,
    then returns the result in json format
    """
    get_profile = Profile.objects.get(user_id=request.user.id)
    get_country = Country.objects.get(name=get_profile.country)

    stream_list = ''
    stream_list_query = list(get_profile.streams.all().values())

    if type == 0:
        type = 'Movies'
        mandatory_filter = '&include_video=false'
    else:
        type = 'TV Shows'
        mandatory_filter = '&include_null_first_air_dates=false'

    for stream in stream_list_query:
        stream_list += (str(stream['provider_id']) + '|')
    page = 1

    ENDPOINT_POPULAR_TITLES = (
        f'include_adult=false{mandatory_filter}&language=en-US&page={page}' +
        f'&sort_by=popularity.desc&watch_region={get_country.country_iso}' +
        f'&with_watch_providers={stream_list[:-1]}'
    )
    if (type == 'Movies'):
        url = (
            f'{BASE_URL}{DISCOVER_MOVIE}?api_key={API_KEY}' +
            '&{ENDPOINT_POPULAR_TITLES}'
        )
    else:
        url = (
            f'{BASE_URL}{DISCOVER_SHOW}?api_key={API_KEY}' +
            f'&{ENDPOINT_POPULAR_TITLES}'
        )
    headers = {
        "accept": "application/json",
    }
    response = requests.get(url, headers=headers)
    pages_count = response.json()['total_pages']

    if pages_count > 1:
        random_number = random.randint(1, pages_count)
    else:
        random_number = 1

    page = random_number

    if (type == 'Movies'):
        url = (
            f'{BASE_URL}{DISCOVER_MOVIE}?api_key={API_KEY}' +
            f'&{ENDPOINT_POPULAR_TITLES}'
        )
    else:
        url = (
            f'{BASE_URL}{DISCOVER_SHOW}?api_key={API_KEY}' +
            f'&{ENDPOINT_POPULAR_TITLES}'
        )

    response = requests.get(url, headers=headers)
    result_initial = response.json()['results']
    result = response.json()['results']

    dont_show = []
    dont_show_list = list(
        MovieOrShow.objects.filter(
            user_id=request.user.id, is_in_dont_show=True
        ).values()
    )
    for title in dont_show_list:
        dont_show.append(title['title_id'])

    for index, title in enumerate(result_initial):
        if title['id'] in dont_show:
            result.remove(title)

    return result


@login_required
def roulette_list(request):
    """
    Main view that controls loadind the roulette
    Recieves data from a form, calls to an API/ retreaves data from database
    and populates movie roulette with titles

    **Context**

    `source_form`
        Data from roulettes restriction fields
    `in_list`
        List of title instances in the roullete
    'user_data'
        data from Djangos user model
    'profile_data'
        data from profile model

    **Template**

    'saved_viewings/roulette_list.html`
    """
    # get_all = MovieOrShow.objects.all()
    # get_all.delete()
    source_form = RouletteSourceForm(data=request.POST)
    in_list = list(
        MovieOrShow.objects.filter(
            user_id=request.user.id, is_in_roulette=True
        ).values()
    )
    user_data = User.objects.get(pk=request.user.id)
    profile_data = Profile.objects.get(user_id=request.user.id)

    if request.method == "POST":
        if source_form.is_valid():
            source = source_form.cleaned_data["source"]
            type = source_form.cleaned_data["type"]
            print(type)
            type = 0 if type == 'Movies' else 1
            print(type)
            load_all = source_form.cleaned_data["load_all"]
            if (source == 'Random'):
                result = tmdb_api_connect(request, type)
            elif (source == 'Favourites'):
                result = list(
                    MovieOrShow.objects.filter(
                        user_id=request.user.id,
                        is_in_favourites=True,
                        type=type
                    ).values()
                )
            elif (source == 'Watchlist'):
                result = list(
                    MovieOrShow.objects.filter(
                        user_id=request.user.id,
                        is_in_watchlist=True,
                        type=type
                        ).values()
                )
            else:
                result = list(MovieOrShow.objects.filter(
                    user_id=request.user.id, is_in_seen_it=True).values()
                )
            roulette_load(request, result, source_form, source, type, load_all)

    in_list = list(
        MovieOrShow.objects.filter(
            user_id=request.user.id, is_in_roulette=True
        ).values()
    )
    empty_card_count = range(5 - len(in_list))

    return render(
        request,
        'saved_viewings/roulette_list.html',
        {
            'source_form': source_form,
            'POSTER_PATH': POSTER_PATH,
            "profile_data": profile_data,
            "user_data": user_data,
            'in_list': in_list,
            'empty_card_count': empty_card_count
        })


@login_required
def roulette_load(request, result, source_form, source, type, load_all):
    """
    Loads MovieOrShow entity with titles if there's less
    that 5 titles in the roulette Uses source_form boolean
    field to determine weather to load all roulette items
    or just one.

    **Context**

    `source_form`
        Data from roulettes restriction fields

    **Template**

    'saved_viewings/roulette_list.html`
    """
    while True:
        if (len(result) > 0):
            if (source == 'Random'):
                random_number = random.randint(1, len(result)-1)
                result_pick = result[random_number]
            else:
                random_number = random.randint(1, len(result)) - 1
                result_pick = result[random_number]
                result_pick['id'] = result_pick['title_id']

            in_list = list(MovieOrShow.objects.filter(
                user_id=request.user.id, is_in_roulette=True).values()
            )
            if len(in_list) == 0:
                add_title_instance(request, result, result_pick, source, type)
                if load_all is False:
                    return False

            elif len(in_list) < 5:
                for title in in_list:
                    if result_pick['id'] == title['title_id']:
                        pass
                    else:
                        add_title_instance(
                            request, result, result_pick, source, type
                        )
                        if load_all is False:
                            return False

            else:
                return False

        else:
            return False

    return render(
        request,
        'saved_viewings/roulette_list.html',
        {
            'source_form': source_form,
        })


@login_required
def roulette_clear(request):
    """
    Queries database and filters for titles in roulette list.
    If the titles aren't in any other lists - title is deleted
    Returns to roulette page
    """
    if request.method == 'POST':
        get_query = MovieOrShow.objects.filter(
            user_id=request.user.id, is_in_roulette=True
        )

        get_list = list(get_query.values())
        get_query.update(is_in_roulette=False)
        for list_item in get_list:
            if (
                list_item['is_in_favourites'] or
                list_item['is_in_watchlist'] or
                list_item['is_in_seen_it'] or
                list_item['is_in_dont_show']
            ) is True:
                pass
            else:
                get_title = MovieOrShow.objects.filter(
                    user_id=request.user.id, title_id=list_item['title_id']
                )
                get_title.delete()

        return HttpResponseRedirect(reverse('roulette_list'))

    return HttpResponseRedirect(reverse('roulette_list'))


@login_required
def clear_one_title(request, title_id):
    """
    Removes a single title to the  roulette carousel
    Redirects to roulete page
    """
    if request.method == 'POST':
        get_title = MovieOrShow.objects.filter(
            user_id=request.user.id, title_id=title_id
            )
        update_title = get_title.update(is_in_roulette=False)
        clear_title(request, get_title, title_id)

        return HttpResponseRedirect(reverse('roulette_list'))

    return HttpResponseRedirect(reverse('roulette_list', args=[title_id]))
