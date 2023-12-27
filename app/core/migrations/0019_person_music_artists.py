# Generated by Django 5.0 on 2023-12-27 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_person_prefix'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='music_artists',
            field=models.ManyToManyField(blank=True, related_name='+', through='core.MusicArtistXPerson', to='core.musicartist'),
        ),
    ]