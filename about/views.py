from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from .models import About
from .forms import ContactForm


@login_required
def about_movie_roulette(request):
    """
    Renders the About page

    **Context**

    `about`
        Data from About model
    `contact_form`
        Data from contact form

    **Templates**

    'about/about.html`
    """
    if request.method == "POST":
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            contact_form.save()

    about = About.objects.all().order_by('-updated_on').first()
    contact_form = ContactForm()

    if request.user.is_active:
        user_data = User.objects.get(pk=request.user.id)
        profile_data = Profile.objects.get(user_id=request.user.id)

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
    
    else:
        return render(
            request,
            "about/about.html",
            {
                "about": about,
                "contact_form": contact_form
            },
        )


@login_required
def index(request):
    """
    Renders index page
    """
    return render(request, "about/index.html")