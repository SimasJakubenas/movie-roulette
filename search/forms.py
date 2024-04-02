from django import forms
from django.db import models
from django.contrib.auth.models import User


class SearchForm(forms.Form):
    YEAR_CHOICES = (
        ('1970s', '1970s'),
        ('1980s', '1980s'),
        ('1990s', '1990s'),
        ('2000s', '2000s'),
        ('2010s', '2010s'),
        ('2020+', '2020+'),
        ('all', 'all')
        )

    RATING_CHOICES = {
        ('*5>', '*5>'),
        ('*5 - *6', '*5 - *6'),
        ('*6 - *7', '*6 - *7'),
        ('*7 - *8', '*7 - *8'),
        ('*8<', '*8<'),
        ('all', 'all')
    }

    RUNTIME_CHOICES = (
        ('60min>', '60min>'),
        ('60min-90min', '60min-90min'),
        ('90min-120min', '90min-120min'),
        ('120min-150min', '120min-150min'),
        ('150min+', '150min+'),
        ('all', 'all'),
        )

    year = forms.CharField(
        widget=forms.Select(
            choices=YEAR_CHOICES,
            attrs={'class': 'browser-default m12'}),
        required=False
    )
    rating = forms.CharField(
        widget=forms.Select(
            choices=RATING_CHOICES,
            attrs={'class': 'browser-default m12'}),
    )
    runtime = forms.CharField(
        widget=forms.Select(
            choices=RUNTIME_CHOICES,
            attrs={'class': 'browser-default m12'}),
        required=False
    )
    cast = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cast'].widget.attrs.update({
            'class': 'form-input'
        })
