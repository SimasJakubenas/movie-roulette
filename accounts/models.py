from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
from saved_viewings.models import StreamingService


class Country(models.Model):
    country_iso = models.CharField(
        primary_key=True, unique=True, max_length=50
    )
    name = models.CharField(max_length=50, null=True, blank=True)
    streams = models.ManyToManyField(
        StreamingService, related_name="countries"
    )

    def __str__(self):
        return self.name


class Profile(models.Model):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="profile_country",
        null=True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = CloudinaryField(
        'Profile picture',
        default='placeholder',
        blank=True,
        null=True
    )
    created_on = models.DateTimeField(auto_now_add=True)
    streams = models.ManyToManyField(
        StreamingService, related_name="Profiles"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
