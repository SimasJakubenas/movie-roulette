import requests
import random
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
    def __init__(self, release_year_min, release_year_max, rating_min, rating_max, runtime_min, runtime_max):
        self.release_year_min = release_year_min
        self.release_year_max = release_year_max
        self.rating_min = rating_min
        self.rating_max = rating_max
        self.runtime_min = runtime_min
        self.runtime_max = runtime_max


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

    rating = request.GET.get('rating')
    search_sorting_rating(rating)

    runtime = request.GET.get('runtime')
    search_sorting_runtime(runtime)

    age_limit = request.GET.get('age_limit')
    
    url = (
        f'{BASE_URL}{DISCOVER_MOVIE}' +
        f'?api_key={API_KEY}' +
        '&include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc' +
        f'{SearchFilterValues.release_year_min}{SearchFilterValues.release_year_max}' +
        f'{SearchFilterValues.rating_min}{SearchFilterValues.rating_max}' +
        f'{SearchFilterValues.runtime_min}{SearchFilterValues.runtime_max}'
        )
    headers = {
        "accept": "application/json",
    }
    response = requests.get(url, headers=headers)
    pages_count = response.json()['total_pages']

    random_number = random.randint(0, pages_count)

    url2 = (
        f'{BASE_URL}{DISCOVER_MOVIE}' +
        f'?api_key={API_KEY}' +
        f'&include_adult=false&include_video=false&language=en-US&page={random_number}&sort_by=popularity.desc' +
        f'{SearchFilterValues.release_year_min}{SearchFilterValues.release_year_max}' +
        f'{SearchFilterValues.rating_min}{SearchFilterValues.rating_max}' +
        f'{SearchFilterValues.runtime_min}{SearchFilterValues.runtime_max}'
    )
    response2 = requests.get(url2, headers=headers)
    search_result = response2.json()['results']
    print(random_number)

    return render(
        request,
        'search/search_results.html',
        {
            'search_result': search_result,
            'POSTER_PATH': POSTER_PATH
        }
    )


def search_sorting_year(year):
    """
    Changes SearchFilterValues class attributes based on 'year' select element
    """
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
    if year == 'all':
        SearchFilterValues.release_year_min = ''
        SearchFilterValues.release_year_max = ''


def search_sorting_rating(rating):
    """
    Changes SearchFilterValues class attributes based on 'rating' select element
    """
    if rating == '*5>':
        SearchFilterValues.rating_min = ''
        SearchFilterValues.rating_max = '&vote_average.lte=4.9'
    if rating == '*5 - *6':
        SearchFilterValues.rating_min = '&vote_average.gte=5'
        SearchFilterValues.rating_max = '&vote_average.lte=5.9'
    if rating == '*6 - *7':
        SearchFilterValues.rating_min = '&vote_average.gte=6'
        SearchFilterValues.rating_max = '&vote_average.lte=6.9'
    if rating == '*7 - *8':
        SearchFilterValues.rating_min = '&vote_average.gte=7'
        SearchFilterValues.rating_max = '&vote_average.lte=7.9'
    if rating == '*8<':
        SearchFilterValues.rating_min = '&vote_average.gte=8'
        SearchFilterValues.rating_max = ''
    if rating == 'all':
        SearchFilterValues.rating_min = ''
        SearchFilterValues.rating_max = ''


def search_sorting_runtime(runtime):
    """
    Changes SearchFilterValues class attributes based on 'runtime' select element
    """
    if runtime == '60min>':
        SearchFilterValues.runtime_min = ''
        SearchFilterValues.runtime_max = '&with_runtime.lte=60'
    if runtime == '60min-90min':
        SearchFilterValues.runtime_min = '&with_runtime.gte=60'
        SearchFilterValues.runtime_max = '&with_runtime.lte=90'
    if runtime == '90min-120min':
        SearchFilterValues.runtime_min = '&with_runtime.gte=90'
        SearchFilterValues.runtime_max = '&with_runtime.lte=120'
    if runtime == '120min-150min':
        SearchFilterValues.runtime_min = '&with_runtime.gte=120'
        SearchFilterValues.runtime_max = '&with_runtime.lte=150'
    if runtime == '150min+':
        SearchFilterValues.runtime_min = '&with_runtime.gte=150'
        SearchFilterValues.runtime_max = ''
    if runtime == 'all':
        SearchFilterValues.runtime_min = ''
        SearchFilterValues.runtime_max = ''