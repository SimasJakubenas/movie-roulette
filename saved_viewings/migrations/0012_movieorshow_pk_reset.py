# Generated by Django 3.2 on 2024-03-31 19:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('saved_viewings', '0011_movieorshow_remove'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieOrShow',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title_id', models.IntegerField()),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(null=True)),
                ('tmdb_rating', models.FloatField(null=True)),
                ('type', models.IntegerField(choices=[(0, 'Movie'), (1, 'TV-Show')], default=0)),
                ('date', models.CharField(blank=True, max_length=30, null=True)),
                ('runtime', models.IntegerField(blank=True, null=True)),
                ('seasons', models.IntegerField(blank=True, null=True)),
                ('age_limit', models.CharField(blank=True, max_length=30, null=True)),
                ('status', models.CharField(blank=True, max_length=30, null=True)),
                ('poster_link', models.CharField(blank=True, max_length=200, null=True)),
                ('backdrop_link', models.CharField(blank=True, max_length=200, null=True)),
                ('is_in_favourites', models.BooleanField(default=False)),
                ('is_in_watchlist', models.BooleanField(default=False)),
                ('is_in_seen_it', models.BooleanField(default=False)),
                ('is_in_dont_show', models.BooleanField(default=False)),
                ('is_in_roulette', models.BooleanField(default=False)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='actor',
            name='titles',
            field=models.ManyToManyField(related_name='actors', to='saved_viewings.MovieOrShow'),
        ),
        migrations.AddField(
            model_name='creator',
            name='titles',
            field=models.ManyToManyField(related_name='creators', to='saved_viewings.MovieOrShow'),
        ),
        migrations.AddField(
            model_name='director',
            name='titles',
            field=models.ManyToManyField(related_name='directors', to='saved_viewings.MovieOrShow'),
        ),
        migrations.AddField(
            model_name='genre',
            name='titles',
            field=models.ManyToManyField(related_name='genres', to='saved_viewings.MovieOrShow'),
        ),
        migrations.AddField(
            model_name='streamingservice',
            name='of_title',
            field=models.ManyToManyField(related_name='streaming_services', to='saved_viewings.MovieOrShow'),
        ),
    ]
