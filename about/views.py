from django.shortcuts import render
from django.contrib.auth.models import User
from accounts.models import Profile
from .models import About
from .forms import ContactForm


def about_movie_roulette(request):
    """
    Renders the About page
    """

    user_data = User.objects.get(pk=request.user.id)
    profile_data = Profile.objects.get(user_id=request.user.id)

    if request.method == "POST":
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            contact_form.save()

    about = About.objects.all().order_by('-updated_on').first()
    contact_form = ContactForm()

    return render(
        request,
        "about/about.html",
        {
            "about": about,
            "profile_data": profile_data,
            "user_data": user_data,
            "contact_form": contact_form
        },
    )


def index(request):
    user_data = User.objects.get(pk=request.user.id)
    profile_data = Profile.objects.get(user_id=request.user.id)

    return render(
        request,
        "about/index.html",
        {
            "profile_data": profile_data,
            "user_data": user_data
        }
    )