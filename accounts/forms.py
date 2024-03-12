from django import forms
from django.db import models
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm, LoginForm
from saved_viewings.models import StreamingService
from .models import Country, Profile
from saved_viewings.models import StreamingService


class CustomSigninForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({
            'class': 'col l7 push-l1 s12 form-input',
            'required': 'required'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'col l7 push-l1 s12 form-input',
            'required' : 'required'
        })


class CustomSignUpForm(SignupForm):

    class Meta:
        model = Profile
        fields = "__all__"

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        widget=forms.Select(attrs={
            'class': "browser-default"
        })
    )
    streams = forms.ModelMultipleChoiceField(
        queryset=StreamingService.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': "browser-default"
        })
    )

    def save(self, *args, **kwargs):
 
        user = super().save(*args, **kwargs)
        new_profile = Profile.objects.create(
            user=user,
            first_name=self.cleaned_data.get("first_name"),
            last_name=self.cleaned_data.get("last_name"),
            country=self.cleaned_data.get("country")
        )

        selected_streams = self.cleaned_data.get('streams')
        get_streams = StreamingService.objects.filter(provider_id__in=selected_streams)
        new_profile.streams.set(get_streams)

        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-input'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-input'
        })
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': ''
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': ''
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': ''
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': ''
        })
        