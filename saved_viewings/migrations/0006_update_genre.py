# Generated by Django 3.2.23 on 2024-02-29 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saved_viewings', '0005_add_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='titles',
            field=models.ManyToManyField(related_name='genres', to='saved_viewings.MovieOrShow'),
        ),
    ]
