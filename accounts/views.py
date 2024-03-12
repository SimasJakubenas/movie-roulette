import requests
from django.shortcuts import render
from saved_viewings.models import StreamingService


def load_providers(request):
    country_iso = request.GET.get('country')
    services = StreamingService.objects.filter(countries__country_iso=country_iso)

    return render(request, 'services_list_options.html', {'services': services})
