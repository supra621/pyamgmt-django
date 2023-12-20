# Generated by Django 5.0 on 2023-12-20 04:27

import django.db.models.deletion
import django_base.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_musicalbumeditionxsongrecording_songrecording_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MusicTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('name', django_base.models.fields.LowerCharField(max_length=31, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MusicArtistXMusicTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('music_artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='music_artist_x_music_tag_set', related_query_name='music_artist_x_music_tag', to='core.musicartist')),
                ('music_tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='music_artist_x_music_tag_set', related_query_name='music_artist_x_music_tag', to='core.musictag')),
            ],
        ),
        migrations.CreateModel(
            name='MusicAlbumXMusicTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('music_album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='music_album_x_music_tag_set', related_query_name='music_album_x_music_tag', to='core.musicalbum')),
                ('music_tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='music_album_x_music_tag_set', related_query_name='music_album_x_music_tag', to='core.musictag')),
            ],
        ),
        migrations.AddConstraint(
            model_name='musicartistxmusictag',
            constraint=models.UniqueConstraint(fields=('music_artist', 'music_tag'), name='unique_music_artist_x_music_tag'),
        ),
        migrations.AddConstraint(
            model_name='musicalbumxmusictag',
            constraint=models.UniqueConstraint(fields=('music_album', 'music_tag'), name='unique_music_album_x_music_tag'),
        ),
    ]
