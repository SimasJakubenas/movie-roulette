import requests
from django.shortcuts import render
from django.contrib.auth.models import User
from saved_viewings.views import API_KEY, BASE_URL, POSTER_BASE_URL, ENDPOINT_POPULAR_TITLES, DISCOVER_MOVIE
from accounts.models import Profile


def movie_releases(request):

    url = f"{BASE_URL}{DISCOVER_MOVIE}?api_key={API_KEY}&{ENDPOINT_POPULAR_TITLES}"
    headers = {
        "accept": "application/json",
    }
    response = requests.get(url, headers=headers)
    movies = response.json()['results']
    user_data = User.objects.get(pk=request.user.id)
    profile_data = Profile.objects.get(user_id=request.user.id)

    return render(
        request,
        "releases/movies.html",
        {
            "movies": movies,
            "profile_data": profile_data,
            "user_data": user_data,
            "POSTER_BASE_URL": POSTER_BASE_URL
        }
    )