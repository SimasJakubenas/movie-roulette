import uuid
from django.db import models
from django.contrib.auth.models import User

TYPE = ((0, "Movie"), (1, "TV-Show"))


class MovieOrShow(models.Model):
    """
    Main entity for storing movie and show instances
    """
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    title_id = models.IntegerField()
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
    """
    Model to store title genres has a bridge table with MovieOrShow entity
    """
    genre_id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    titles = models.ManyToManyField(
        MovieOrShow, related_name="genres"
    )

    def __str__(self):
        return self.name


class Person(models.Model):
    """
    Stores all cast and crew data
    """
    person_id = models.IntegerField(primary_key=True, unique=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)


class Actor(models.Model):
    """
    Model to store actors instances. Has a bridge table with
    MovieOrShow entity
    """
    actor_id = models.CharField(primary_key=True, unique=True, max_length=50)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    titles = models.ManyToManyField(
        MovieOrShow, related_name="actors"
    )


class Director(models.Model):
    """
    Model to store directors instances. Has a bridge table with
    MovieOrShow entity
    """
    director_id = models.CharField(
        primary_key=True, unique=True, max_length=50
        )
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    titles = models.ManyToManyField(
        MovieOrShow, related_name="directors"
    )


class Creator(models.Model):
    """
    Model to store creator instances. Has a bridge table with
    MovieOrShow entity
    """
    creator_id = models.CharField(primary_key=True, unique=True, max_length=50)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    titles = models.ManyToManyField(
        MovieOrShow, related_name="creators"
    )


class StreamingService(models.Model):
    """
    Model to store users streaming services and also titles streaming
    services. Has a bridge table with MovieOrShow entity
    """
    provider_id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    logo_path = models.CharField(max_length=200, null=True, blank=True)
    of_title = models.ManyToManyField(
        MovieOrShow, related_name="streaming_services"
    )

    def __str__(self):
        return self.name
