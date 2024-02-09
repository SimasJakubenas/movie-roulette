from django.shortcuts import render
from django.views import generic
# from .models import MovieOrShow
from .forms import RouletteSourceForm

# Create your views here.
# class TitleList(generic.ListView):
#     queryset = MovieOrShow.objects.all()


def roulette_list(request):
    source = RouletteSourceForm()
    return render(request, 'saved_viewings/roulette_list.html', {'source': source})
    
