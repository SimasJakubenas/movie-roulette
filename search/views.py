import requests
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from saved_viewings.views import API_KEY, BASE_URL, POSTER_PATH, DISCOVER_MOVIE, DISCOVER_SHOW
from saved_viewings.models import StreamingService, MovieOrShow
from accounts.models import Profile
from .forms import SearchForm


class SearchFilterValues:
    """
    Class used to store API filters based of user input from a search page
    """
    def __init__(self, release_year_min, release_year_max):
        self.release_year_min = release_year_min
        self.release_year_max = release_year_max


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
    year = request.GET.get('year')
    search_sorting_year(year)

    rating = request.POST.get('rating')
    runtime = request.POST.get('runtime')
    age_limit = request.POST.get('age_limit')
    
    url = (
        f'{BASE_URL}{DISCOVER_MOVIE}' +
        f'?api_key={API_KEY}' +
        '&include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc' +
        f'{SearchFilterValues.release_year_min}{SearchFilterValues.release_year_max}'
        )
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


def search_sorting_year(year):
    if year == '1970s':
        SearchFilterValues.release_year_min = '&primary_release_date.gte=1970-01-01'
        SearchFilterValues.release_year_max = '&primary_release_date.lte=1979-12-31'
    if year == '1980s':
        SearchFilterValues.release_year_min = '&primary_release_date.gte=1980-01-01'
        SearchFilterValues.release_year_max = '&primary_release_date.lte=1989-12-31'
    if year == '1990s':
        SearchFilterValues.release_year_min = '&primary_release_date.gte=1990-01-01'
        SearchFilterValues.release_year_max = '&primary_release_date.lte=1999-12-31'
    if year == '2000s':
        SearchFilterValues.release_year_min = '&primary_release_date.gte=2000-01-01'
        SearchFilterValues.release_year_max = '&primary_release_date.lte=2009-12-31'
    if year == '2010s':
        SearchFilterValues.release_year_min = '&primary_release_date.gte=2010-01-01'
        SearchFilterValues.release_year_max = '&primary_release_date.lte=2019-12-31'
    if year == '2020+':
        SearchFilterValues.release_year_min = '&primary_release_date.gte=2020-01-01'
    if year == 'all+':
        SearchFilterValues.release_year_min = ''
        SearchFilterValues.release_year_max = ''


