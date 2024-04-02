import requests
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from saved_viewings.views import (
    API_KEY,
    BASE_URL,
    POSTER_BASE_URL,
    DISCOVER_MOVIE,
    DISCOVER_SHOW
)
from saved_viewings.models import StreamingService, MovieOrShow
from accounts.models import Profile, Country


@login_required
def movie_releases(request):
    """
    Calls multiple API endpoints to fetch data
    Querys django user model/ profile model for logged in user
    renders movie page and passes all the data

    **Context**

    `source_form`
        Data from roulettes restriction fields
    `in_list`
        List of title instances in the fsvourites list

    **Templates**

    'releases/movies.html`
    """
    get_profile = Profile.objects.get(user_id=request.user.id)
    get_country = Country.objects.get(name=get_profile.country)
    stream_list = ''
    stream_list_query = list(get_profile.streams.all().values())
    for stream in stream_list_query:
        stream_list += (str(stream['provider_id']) + '|')

    ENDPOINT_POPULAR_TITLES = (
        'include_adult=false&language=en-US&page=1&sort_by=popularity.desc' +
        f'&watch_region={get_country.country_iso}' +
        f'&with_watch_providers={stream_list[:-1]}'
    )
    url_discover = (
        f"{BASE_URL}{DISCOVER_MOVIE}?api_key={API_KEY}&{ENDPOINT_POPULAR_TITLES}"
    )
    url_popular = (
        f"{BASE_URL}/movie/popular?api_key={API_KEY}&{ENDPOINT_POPULAR_TITLES}"
    )
    url_top_rated = (
        f"{BASE_URL}/movie/top_rated?api_key={API_KEY}&{ENDPOINT_POPULAR_TITLES}"
    )
    headers = {
        "accept": "application/json",
    }
    response_discover = requests.get(url_discover, headers=headers)
    response_popular = requests.get(url_popular, headers=headers)
    response_top_rated = requests.get(url_top_rated, headers=headers)

    movies_discover = response_discover.json()['results']
    movies_discover_amemded = response_discover.json()['results']
    movies_popular = response_popular.json()['results']
    movies_popular_amended = response_popular.json()['results']
    movies_top_rated = response_top_rated.json()['results']
    movies_top_rated_amended = response_top_rated.json()['results']

    dont_show = []
    get_user = User.objects.get(pk=request.user.id)
    dont_show_list = list(
        MovieOrShow.objects.filter(user_id=request.user.id, is_in_dont_show=True).values()
        )
    for title in dont_show_list:
        dont_show.append(title['title_id'])

    for index, movie in enumerate(movies_discover):
        if movie['id'] in dont_show:
            movies_discover_amemded.remove(movie)

    for index, movie in enumerate(movies_popular):
        if movie['id'] in dont_show:
            movies_popular_amended.remove(movie)

    for index, movie in enumerate(movies_top_rated):
        if movie['id'] in dont_show:
            movies_top_rated_amended.remove(movie)

    user_data = User.objects.get(pk=request.user.id)
    profile_data = Profile.objects.get(user_id=request.user.id)

    return render(
        request,
        "releases/movies.html",
        {
            "movies_discover": movies_discover_amemded,
            "movies_popular": movies_popular_amended,
            "movies_top_rated": movies_top_rated_amended,
            "profile_data": profile_data,
            "user_data": user_data,
            "POSTER_BASE_URL": POSTER_BASE_URL
        }
    )


@login_required
def show_releases(request):
    """
    Calls multiple API endpoints to fetch data
    Querys django user model/ profile model for logged in user
    renders shows page, filters the data recieved to exclude
     titles in don't show page and passes updated data to page

    **Context**

    `source_form`
        Data from roulettes restriction fields
    `in_list`
        List of title instances in the fsvourites list

    **Templates**

    'releases/shows.html`
    """
    get_profile = Profile.objects.get(user_id=request.user.id)
    get_country = Country.objects.get(name=get_profile.country)
    stream_list = ''
    stream_list_query = list(get_profile.streams.all().values())
    for stream in stream_list_query:
        stream_list += (str(stream['provider_id']) + '|')
    ENDPOINT_POPULAR_TITLES = (
        'include_adult=false&language=en-US&page=1&sort_by=popularity.desc' +
        f'&include_null_first_air_dates=false&watch_region={get_country.country_iso}' +
        f'&with_watch_providers={stream_list[:-1]}'
    )
    url_discover = (
        f"{BASE_URL}{DISCOVER_SHOW}?api_key={API_KEY}&{ENDPOINT_POPULAR_TITLES}"
    )
    url_popular = (
        f"{BASE_URL}/tv/popular?api_key={API_KEY}&{ENDPOINT_POPULAR_TITLES}"
    )
    url_top_rated = (
        f"{BASE_URL}/tv/top_rated?api_key={API_KEY}&{ENDPOINT_POPULAR_TITLES}"
    )
    
    headers = {
        "accept": "application/json",
    }
    response_discover = requests.get(url_discover, headers=headers)
    response_popular = requests.get(url_popular, headers=headers)
    response_top_rated = requests.get(url_top_rated, headers=headers)

    shows_discover = response_discover.json()['results']
    shows_discover_amemded = response_discover.json()['results']
    shows_popular = response_popular.json()['results']
    shows_popular_amended = response_popular.json()['results']
    shows_top_rated = response_top_rated.json()['results']
    shows_top_rated_amended = response_top_rated.json()['results']

    dont_show = []
    dont_show_list = list(
        MovieOrShow.objects.filter(user_id=request.user.id, is_in_dont_show=True).values()
        )
    for title in dont_show_list:
        dont_show.append(title['title_id'])

    for index, show in enumerate(shows_discover):
        if show['id'] in dont_show:
            shows_discover_amemded.remove(show)

    for index, show in enumerate(shows_popular):
        if show['id'] in dont_show:
            shows_popular_amended.remove(show)

    for index, show in enumerate(shows_top_rated):
        if show['id'] in dont_show:
            shows_top_rated_amended.remove(show)
    user_data = User.objects.get(pk=request.user.id)
    profile_data = Profile.objects.get(user_id=request.user.id)

    return render(
        request,
        "releases/shows.html",
        {
            "shows_discover": shows_discover_amemded,
            "shows_popular": shows_popular_amended,
            "shows_top_rated": shows_top_rated_amended,
            "profile_data": profile_data,
            "user_data": user_data,
            "POSTER_BASE_URL": POSTER_BASE_URL
        }
    )
