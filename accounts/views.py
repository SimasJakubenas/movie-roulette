import requests
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from saved_viewings.models import StreamingService
from saved_viewings.views import POSTER_BASE_URL
from .models import Profile
from .forms import ProfileImage, CustomSignUpForm, EditProfileForm


def load_providers(request):
    country_iso = request.GET.get('country')
    services = StreamingService.objects.filter(countries__country_iso=country_iso)

    return render(request, 'services_list_options.html', {'services': services})


def profile_page(request):

    user_data = User.objects.get(pk=request.user.id)
    profile_data = Profile.objects.get(user_id=request.user.id)
    profile_streams = profile_data.streams.all()
    profile_img = ProfileImage(request.POST)

    return render(
        request,
        "accounts/profile.html",
        {
            "profile_data": profile_data,
            "user_data": user_data,
            "profile_streams": profile_streams,
            "POSTER_BASE_URL": POSTER_BASE_URL,
            "profile_img": profile_img
        }
    )


def update_profile_pic(request):
    """
    Accquires profile picture data from a suubmitted form and
    updates Profile model.
    Returns back to profile page
    """
    if request.method == "POST":
        profile_pic = ProfileImage(request.POST, request.FILES)
        
        if profile_pic.is_valid():
            profile_pic_url = profile_pic.cleaned_data["profile_pic"]
            update_picture = Profile.objects.get(user_id=request.user.id)
            update_picture.profile_pic = profile_pic_url
            update_picture.save()
            
    profile_pic = ProfileImage()

    return HttpResponseRedirect(reverse('profile'))


def edit_profile(request):
    """
    Updates the user profile by using the input data through
    EditProfileForm form.
    Renders 'accounts/edit_profile.html' template
    """
    user_data = User.objects.get(pk=request.user.id)
    profile_data = Profile.objects.get(user_id=request.user.id)
    profile_streams = profile_data.streams.all()
    
    if request.method == "POST":
        form = EditProfileForm(request.POST)

        if form.is_valid():
            print(profile_data.first_name)
            user_data.first_name = form.cleaned_data["first_name"]
            user_data.last_name = form.cleaned_data["last_name"]
            selected_streams = form.cleaned_data.get('streams')
            get_streams = StreamingService.objects.filter(provider_id__in=selected_streams)
            profile_data.streams.set(get_streams)
            user_data.save()
            profile_data.save()

            return HttpResponseRedirect(reverse('profile'))
        
        return render(
            request,
            "accounts/edit_profile.html",
            {
                "profile_data": profile_data,
                "profile_streams": profile_streams,
                "user_data": user_data,
                "POSTER_BASE_URL": POSTER_BASE_URL,
                "form": form
            }
        )
    
    form = CustomSignUpForm()

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "profile_data": profile_data,
            "profile_streams": profile_streams,
            "user_data": user_data,
            "POSTER_BASE_URL": POSTER_BASE_URL,
            "form": form
        }
    )


def delete_profile(request):
    """
    Deletes user instance
    """
    get_user = User.objects.get(pk=request.user.id)
    get_user.delete()

    return redirect("home")