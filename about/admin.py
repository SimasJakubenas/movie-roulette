from django.contrib import admin
from .models import About, ContactFormModel
from django_summernote.admin import SummernoteModelAdmin


@admin.register(About)
class AboutAdmin(SummernoteModelAdmin):

    summernote_fields = ('content',)


@admin.register(ContactFormModel)
class ContactFormModelAdmin(admin.ModelAdmin):

    list_display = ('message', 'read',)
