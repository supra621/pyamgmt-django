# Generated by Django 5.0 on 2023-12-18 03:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_book_series_catalogitembookpublication'),
    ]

    operations = [
        migrations.CreateModel(
            name='MusicAlbumXVideoGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('music_album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='music_album_x_video_game_set', related_query_name='music_album_x_video_game', to='core.musicalbum')),
                ('video_game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='music_album_x_video_game_set', related_query_name='music_album_x_video_game', to='core.videogame')),
            ],
        ),
        migrations.AddConstraint(
            model_name='musicalbumxvideogame',
            constraint=models.UniqueConstraint(fields=('music_album', 'video_game'), name='unique_music_album_x_video_game'),
        ),
    ]
