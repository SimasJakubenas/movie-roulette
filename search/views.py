import requests
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from saved_viewings.views import API_KEY, BASE_URL, POSTER_PATH, DISCOVER_MOVIE, DISCOVER_SHOW
from saved_viewings.models import StreamingService, MovieOrShow
from accounts.models import Profile
from .forms import SearchForm


@login_required
def search_page(request):
    """
    Loads  search page
    """
    search_form = SearchForm(data=request.POST)
    user_data = User.objects.get(pk=request.user.id)
    profile_data = Profile.objects.get(user_id=request.user.id)

    return render(
        request,
        'search/search_page.html',
        {
            'search_form': search_form,
            'user_data': user_data,
            'profile_data': profile_data,
            'POSTER_PATH': POSTER_PATH
        }
    )


@login_required
def search_results(request):
    """
    Loads  search results
    """
    year = request.POST.get('year')
    rating = request.POST.get('rating')
    runtime = request.POST.get('runtime')
    age_limit = request.POST.get('age_limit')
    url = f'{BASE_URL}{DISCOVER_MOVIE}?api_key={API_KEY}&include_adult=false&include_video=false&language=en-US&page=1&primary_release_date.gte=2012'
    headers = {
        "accept": "application/json",
    }
    response = requests.get(url, headers=headers)
    search_result = response.json()['results']

    return render(
        request,
        'search/search_results.html',
        {
            'search_result': search_result,
            'POSTER_PATH': POSTER_PATH
        }
    )
