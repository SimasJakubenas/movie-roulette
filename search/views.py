import requests
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from saved_viewings.views import API_KEY, BASE_URL, POSTER_BASE_URL, DISCOVER_MOVIE, DISCOVER_SHOW
from saved_viewings.models import StreamingService, MovieOrShow
from accounts.models import Profile, Country


@login_required
def search_page(request):
    """
    Loads  search page
    """

    return render(
        request,
        'search_page.html',
        {}
    )
