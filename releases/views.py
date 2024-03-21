import requests
from django.shortcuts import render
from django.contrib.auth.models import User
from saved_viewings.views import API_KEY, BASE_URL, POSTER_BASE_URL, ENDPOINT_POPULAR_TITLES, DISCOVER_MOVIE, DISCOVER_SHOW
from accounts.models import Profile


def movie_releases(request):

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


def show_releases(request):

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