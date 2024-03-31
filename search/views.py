import requests
import random
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from saved_viewings.views import API_KEY, BASE_URL, POSTER_PATH, DISCOVER_MOVIE, DISCOVER_SHOW
from saved_viewings.models import StreamingService, Genre
from accounts.models import Profile, Country
from .forms import SearchForm


class SearchFilterValues:
    """
    Class used to store API filters based of user input from a search page
    """
    def __init__(self, release_year_min, release_year_max, rating_min, rating_max, runtime_min, runtime_max, cast, cast_list, genre):
        self.release_year_min = release_year_min
        self.release_year_max = release_year_max
        self.rating_min = rating_min
        self.rating_max = rating_max
        self.runtime_min = runtime_min
        self.runtime_max = runtime_max
        self.cast = cest
        self.cast_list = cast_list
        self.genre = genre


def search_genres(request):
    type = request.GET.get('type')

    url_genre = (
        f'{BASE_URL}/genre/{type}/list' +
        f'?api_key={API_KEY}'
    )
    headers = {
        "accept": "application/json",
    }
    response_genre = requests.get(url_genre, headers=headers)
    search_genre= response_genre.json()['genres']

    return render(
        request,
        'search/genres.html',
        {'search_genre': search_genre}
        )


@login_required
def search_page(request):
    """
    Loads  search page
    """
    search_form = SearchForm(data=request.POST)
    user_data = User.objects.get(pk=request.user.id)
    profile_data = Profile.objects.get(user_id=request.user.id)
    url_genre = (
        f'{BASE_URL}/genre/movie/list' +
        f'?api_key={API_KEY}'
    )
    headers = {
        "accept": "application/json",
    }
    response_genre = requests.get(url_genre, headers=headers)
    search_genre= response_genre.json()['genres']

    return render(
        request,
        'search/search_page.html',
        {
            'search_form': search_form,
            'user_data': user_data,
            'profile_data': profile_data,
            'POSTER_PATH': POSTER_PATH,
            'search_genre': search_genre
        }
    )


@login_required
def search_results(request):
    """
    Loads  search results
    """
    SearchFilterValues.release_year_min = ''
    SearchFilterValues.release_year_max = ''
    SearchFilterValues.rating_min = ''
    SearchFilterValues.rating_max = ''
    SearchFilterValues.runtime_min = ''
    SearchFilterValues.runtime_max = ''
    SearchFilterValues.cast = ''
    SearchFilterValues.cast_list = ''
    type = request.GET.get('titleType')

    genre_list = request.GET.get('jointGenreList')
    updated_genre_list = genre_list.replace(",", '|')
    print(updated_genre_list)
    if len(genre_list) != 0 :
        SearchFilterValues.genre = f'&with_genres={updated_genre_list}'
    else:
         SearchFilterValues.genre = ''
    print(SearchFilterValues.genre)
    year = request.GET.get('year')
    search_sorting_year(year)

    rating = request.GET.get('rating')
    search_sorting_rating(rating)

    runtime = request.GET.get('runtime')
    search_sorting_runtime(runtime)

    cast = request.GET.get('cast')

    headers = {
        "accept": "application/json",
    }

    if len(cast) > 0:
        SearchFilterValues.cast = '&with_cast='
        cast_split = cast.replace(" ", "+").split(',')
        SearchFilterValues.cast_list = []
        if len(cast_split) > 1:
            for person in cast_split:
                url_cast = (
                    f'{BASE_URL}/search/person' +
                    f'?api_key={API_KEY}' +
                    f'&query={person}'
                )
                response_cast = requests.get(url_cast, headers=headers)
                search_cast= response_cast.json()['results']

                if search_cast != []:
                    SearchFilterValues.cast_list.append(str(search_cast))
            joint_ids = ",".join(str(id) for id in SearchFilterValues.cast_list)
            SearchFilterValues.cast += (str(joint_ids))
        else:
            url_cast = (
                f'{BASE_URL}/search/person' +
                f'?api_key={API_KEY}' +
                f'&query={cast_split}'
            )
            response_cast = requests.get(url_cast, headers=headers)
            search_cast= response_cast.json()['results'][0]['id']
            SearchFilterValues.cast += str(search_cast)

    else:
        SearchFilterValues.cast = ''

    get_profile = Profile.objects.get(user_id=request.user.id)
    stream_list = ''
    stream_list_query = list(get_profile.streams.all().values())

    for stream in stream_list_query:
        stream_list += (str(stream['provider_id']) + '|')
    print(stream_list)
    url = (
        f'{BASE_URL}/discover/{type}' +
        f'?api_key={API_KEY}' +
        '&include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc' +
        f'{SearchFilterValues.release_year_min}{SearchFilterValues.release_year_max}' +
        f'{SearchFilterValues.rating_min}{SearchFilterValues.rating_max}' +
        f'{SearchFilterValues.runtime_min}{SearchFilterValues.runtime_max}' +
        f'{SearchFilterValues.cast}' +
        f'{SearchFilterValues.genre}' +
        f'&with_watch_providers={stream_list[:-1]}'
    )
    response = requests.get(url, headers=headers)
    pages_count = response.json()['total_pages']
    
    if pages_count > 1:
        random_number = random.randint(1, pages_count)
    else:
        random_number = 1

    url2 = (
        f'{BASE_URL}/discover/{type}' +
        f'?api_key={API_KEY}' +
        f'&include_adult=false&include_video=false&language=en-US&page={random_number}&sort_by=popularity.desc' +
        f'{SearchFilterValues.release_year_min}{SearchFilterValues.release_year_max}' +
        f'{SearchFilterValues.rating_min}{SearchFilterValues.rating_max}' +
        f'{SearchFilterValues.runtime_min}{SearchFilterValues.runtime_max}' +
        f'{SearchFilterValues.cast}' +
        f'{SearchFilterValues.genre}' +
        f'&with_watch_providers={stream_list[:-1]}'
    )
    response2 = requests.get(url2, headers=headers)
    search_result2 = response2.json()['results']

    return render(
        request,
        'search/search_results.html',
        {
            'search_result': search_result2,
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