# Generated by Django 5.0 on 2023-12-20 23:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0049_personxsongperformance_songperformance_personnel_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SongArrangement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('is_original', models.BooleanField(default=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='songperformance',
            name='music_artists',
        ),
        migrations.RemoveField(
            model_name='songperformance',
            name='personnel',
        ),
        migrations.RemoveField(
            model_name='songperformance',
            name='song',
        ),
        migrations.AlterField(
            model_name='personxsongperformance',
            name='song_performance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_x_song_performance_set', related_query_name='person_x_song_performance', to='songperformance'),
        ),
        migrations.AlterField(
            model_name='musicartistxsongperformance',
            name='song_performance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='music_artist_x_song_performance_set', related_query_name='music_artist_x_song_performance', to='songperformance'),
        ),
        migrations.RemoveField(
            model_name='songrecording',
            name='song_performance',
        ),
        migrations.CreateModel(
            name='SongXSongArrangement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='song_x_song_arrangement_set', related_query_name='song_x_song_arrangement', to='core.song')),
                ('song_arrangement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='song_x_song_arrangement_set', related_query_name='song_x_song_arrangement', to='core.songarrangement')),
            ],
        ),
        migrations.AddField(
            model_name='songarrangement',
            name='songs',
            field=models.ManyToManyField(related_name='arrangements', through='core.SongXSongArrangement', to='core.song'),
        ),
        migrations.DeleteModel(
            name='SongPerformance',
        ),
        migrations.AddConstraint(
            model_name='songxsongarrangement',
            constraint=models.UniqueConstraint(fields=('song', 'song_arrangement'), name='unique_song_x_song_arrangement'),
        ),
        migrations.AddConstraint(
            model_name='songarrangement',
            constraint=models.UniqueConstraint(fields=('title', 'description'), name='unique_song_arrangement'),
        ),
    ]
