from django.contrib import admin
from .models import MovieOrShow
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
@admin.register(MovieOrShow)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'type')
    search_fields = ['title']
    list_filter = ('type',)
    prepopulated_fields = {'title': ('title',)}
    summernote_fields = ('description',)

