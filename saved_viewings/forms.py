from django.db import models
from django import forms
from .models import MovieOrShow


class RouletteSourceForm(forms.Form):
    SOURCE_CHOICES = (
        ('Random', 'Random'),
        ('Favourites', 'Favourites'),
        ('Watchlist', 'Watchlist'),
        ('Seen It', 'Seen It')
        )
    TYPE_CHOICES = {
        ('Movie', 'Movie'),
        ('TV_Show', 'TV_Show')
    }
    source = forms.CharField(
        widget=forms.Select(
            choices=SOURCE_CHOICES,
            attrs={'class': 'browser-default col xl6 push-xl3 m10 push-m1'}),
    )
    type = forms.CharField(
        widget=forms.Select(
            choices=TYPE_CHOICES,
            attrs={'class': 'browser-default col xl6 push-xl3 m10 push-m1'}),
    )
    # source = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=CHOICES)
