from django.shortcuts import render
from .models import About
from .forms import ContactForm


def about_movie_roulette(request):
    """
    Renders the About page
    """
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
            "contact_form": contact_form
        },
    )