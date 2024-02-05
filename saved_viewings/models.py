from django.db import models
from django.contrib.auth.models import User

TYPE = ((0, "Movie"), (1, "TV-Show"))

# Create your models here.
class MovieOrShow(models.Model):
    title_id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="viewings"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    tmdb_rating = models.FloatField(null=True)
    type = models.IntegerField(choices=TYPE, default=0)
    year = models.IntegerField(null=True)
    runtime = models.IntegerField(null=True)
    seasons = models.IntegerField(null=True)
    age_limit = models.CharField(max_length=30)
    poster_link = models.URLField(max_length=200)
    backdrop_link = models.URLField(max_length=200)