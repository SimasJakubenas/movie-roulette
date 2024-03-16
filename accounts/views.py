import requests
from django.shortcuts import render
from django.contrib.auth.models import User
from saved_viewings.models import StreamingService
from saved_viewings.views import POSTER_BASE_URL
from .models import Profile


def load_providers(request):
    country_iso = request.GET.get('country')
    services = StreamingService.objects.filter(countries__country_iso=country_iso)

    return render(request, 'services_list_options.html', {'services': services})


def profile_page(request):

    user_data = User.objects.get(pk=request.user.id)
    profile_data = Profile.objects.get(user_id=request.user.id)
    profile_streams = profile_data.streams.all()
    print(profile_data.profile_pic)

    return render(
        request,
        "accounts/profile.html",
        {
            "profile_data": profile_data,
            "user_data": user_data,
            "profile_streams": profile_streams,
            "POSTER_BASE_URL": POSTER_BASE_URL
        }
    )