from django.db import models
from django.contrib.auth.models import User

TYPE = ((0, "Movie"), (1, "TV-Show"))


class MovieOrShow(models.Model):
    title_id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="viewings"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    tmdb_rating = models.FloatField(null=True)
    type = models.IntegerField(choices=TYPE, default=0)
    date = models.CharField(max_length=30, null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    seasons = models.IntegerField(null=True, blank=True)
    age_limit = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(max_length=30, null=True, blank=True)
    poster_link = models.CharField(max_length=200, null=True, blank=True)
    backdrop_link = models.CharField(max_length=200, null=True, blank=True)
    is_in_favourites = models.BooleanField(default=False)
    is_in_watchlist = models.BooleanField(default=False)
    is_in_seen_it = models.BooleanField(default=False)
    is_in_dont_show = models.BooleanField(default=False)
    is_in_roulette = models.BooleanField(default=False)


class Genre(models.Model):
    genre_id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    titles =  models.ManyToManyField(
        MovieOrShow, related_name="genres"
    )

    def __str__(self):
        return self.name


class Person(models.Model):
    person_id = models.IntegerField(primary_key=True, unique=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)


class Actor(models.Model):
    actor_id = models.CharField(primary_key=True, unique=True, max_length=50)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    titles =  models.ManyToManyField(
        MovieOrShow, related_name="actors"
    )


class Director(models.Model):
    director_id = models.CharField(primary_key=True, unique=True, max_length=50)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    titles =  models.ManyToManyField(
        MovieOrShow, related_name="directors"
    )


class Creator(models.Model):
    creator_id = models.CharField(primary_key=True, unique=True, max_length=50)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    titles =  models.ManyToManyField(
        MovieOrShow, related_name="creators"
    )

    
class StreamingService(models.Model):
    provider_id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    logo_path = models.CharField(max_length=200, null=True, blank=True)
    of_title =  models.ManyToManyField(
        MovieOrShow, related_name="streaming_services"
    )

    def __str__(self):
        return self.name
    