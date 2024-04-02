from django.contrib import admin
from .models import About, ContactFormModel
from django_summernote.admin import SummernoteModelAdmin


@admin.register(About)
class AboutAdmin(SummernoteModelAdmin):
    """
    Makes About page content editable from admin page
    """
    summernote_fields = ('content',)


@admin.register(ContactFormModel)
class ContactFormModelAdmin(admin.ModelAdmin):
    """
    Makes contact from submisions readable in the admin panel
    """
    list_display = ('message', 'read',)
