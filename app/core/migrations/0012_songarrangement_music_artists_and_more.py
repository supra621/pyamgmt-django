# Generated by Django 5.0 on 2023-12-24 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_recordlabel'),
    ]

    operations = [
        migrations.AddField(
            model_name='songarrangement',
            name='music_artists',
            field=models.ManyToManyField(blank=True, related_name='+', through='core.MusicArtistXSongArrangement', to='core.musicartist'),
        ),
        migrations.AlterField(
            model_name='songarrangement',
            name='songs',
            field=models.ManyToManyField(blank=True, related_name='+', through='core.SongXSongArrangement', to='core.song'),
        ),
    ]
