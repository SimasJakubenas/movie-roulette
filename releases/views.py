import requests
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from saved_viewings.views import API_KEY, BASE_URL, POSTER_BASE_URL, DISCOVER_MOVIE, DISCOVER_SHOW
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
    ENDPOINT_POPULAR_TITLES = f'include_adult=false&language=en-US&page=1&sort_by=popularity.desc&watch_region={get_country.country_iso}&with_watch_providers=8'
    url_discover = f"{BASE_URL}{DISCOVER_MOVIE}?api_key={API_KEY}&{ENDPOINT_POPULAR_TITLES}"
    url_popular = f"{BASE_URL}/movie/popular?api_key={API_KEY}&{ENDPOINT_POPULAR_TITLES}"
    url_top_rated = f"{BASE_URL}/movie/top_rated?api_key={API_KEY}&{ENDPOINT_POPULAR_TITLES}"
    headers = {
        "accept": "application/json",
    }
    response_discover = requests.get(url_discover, headers=headers)
    response_popular = requests.get(url_popular, headers=headers)
    response_top_rated = requests.get(url_top_rated, headers=headers)

    movies_discover = response_discover.json()['results']
    movies_popular = response_popular.json()['results']
    movies_top_rated = response_top_rated.json()['results']

    user_data = User.objects.get(pk=request.user.id)
    profile_data = Profile.objects.get(user_id=request.user.id)

    return render(
        request,
        "releases/movies.html",
        {
            "movies_discover": movies_discover,
            "movies_popular": movies_popular,
            "movies_top_rated": movies_top_rated,
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
    renders shows page and passes all the data

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
    ENDPOINT_POPULAR_TITLES = f'include_adult=false&language=en-US&page=1&sort_by=popularity.desc&watch_region={get_country.country_iso}&with_watch_providers=8'
    url_discover = f"{BASE_URL}{DISCOVER_SHOW}?api_key={API_KEY}&{ENDPOINT_POPULAR_TITLES}"
    url_popular = f"{BASE_URL}/tv/popular?api_key={API_KEY}&{ENDPOINT_POPULAR_TITLES}"
    url_top_rated = f"{BASE_URL}/tv/top_rated?api_key={API_KEY}&{ENDPOINT_POPULAR_TITLES}"
    headers = {
        "accept": "application/json",
    }
    response_discover = requests.get(url_discover, headers=headers)
    response_popular = requests.get(url_popular, headers=headers)
    response_top_rated = requests.get(url_top_rated, headers=headers)

    shows_discover = response_discover.json()['results']
    shows_popular = response_popular.json()['results']
    shows_top_rated = response_top_rated.json()['results']

    user_data = User.objects.get(pk=request.user.id)
    profile_data = Profile.objects.get(user_id=request.user.id)

    return render(
        request,
        "releases/shows.html",
        {
            "shows_discover": shows_discover,
            "shows_popular": shows_popular,
            "shows_top_rated": shows_top_rated,
            "profile_data": profile_data,
            "user_data": user_data,
            "POSTER_BASE_URL": POSTER_BASE_URL
        }
    )