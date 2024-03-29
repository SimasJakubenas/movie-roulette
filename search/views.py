import requests
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from saved_viewings.views import API_KEY, BASE_URL, POSTER_BASE_URL, DISCOVER_MOVIE, DISCOVER_SHOW
from saved_viewings.models import StreamingService, MovieOrShow
from .forms import SearchForm


@login_required
def search_page(request):
    """
    Loads  search page
    """
    search_form = SearchForm(data=request.POST)
    return render(
        request,
        'search/search_page.html',
        {
            'search_form': search_form
        }
    )


@login_required
def search_results(request):
    """
    Loads  search results
    """
    return render(
        request,
        'search/search_page.html',
        {
            
        }
    )
