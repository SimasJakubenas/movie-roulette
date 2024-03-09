from django.db import models
from django import forms
from allauth.account.forms import SignupForm, LoginForm
from .models import MovieOrShow


class CustomSigninForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({
            'class': 'col l7 push-l1 s12 form-input',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'col l7 push-l1 s12 form-input',
        })
        

class RouletteSourceForm(forms.Form):
    SOURCE_CHOICES = (
        ('Random', 'Random'),
        ('Favourites', 'Favourites'),
        ('Watchlist', 'Watchlist'),
        ('Seen It', 'Seen It')
        )
    TYPE_CHOICES = {
        ('Movies', 'Movies'),
        ('TV Shows', 'TV Shows')
    }

    source = forms.CharField(
        widget=forms.Select(
            choices=SOURCE_CHOICES,
            attrs={'class': 'browser-default col xl6 push-xl3 m10 push-m1'}),
            required=False
    )
    type = forms.CharField(
        widget=forms.Select(
            choices=TYPE_CHOICES,
            attrs={'class': 'browser-default col xl6 push-xl3 m10 push-m1'}),
    )
    load_all = forms.BooleanField(required=False)

