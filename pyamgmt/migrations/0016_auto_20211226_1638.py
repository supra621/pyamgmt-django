# Generated by Django 3.2.8 on 2021-12-26 21:38

import deform.db.models.fields.fields
import deform.db.models.fields.related
from django.db import migrations, models
import django.db.models.deletion
import pyamgmt.validators


class Migration(migrations.Migration):

    dependencies = [
        ('pyamgmt', '0015_auto_20211028_0108'),
    ]

    operations = [
        migrations.CreateModel(
            name='MusicAlbumToSongRecording',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_created', deform.db.models.fields.fields.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', deform.db.models.fields.fields.DateTimeField(auto_now=True)),
                ('disc_number', deform.db.models.fields.fields.PositiveSmallIntegerField(blank=True, null=True)),
                ('track_number', deform.db.models.fields.fields.PositiveSmallIntegerField(blank=True, null=True)),
                ('musicalbum', deform.db.models.fields.related.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pyamgmt.musicalbum')),
            ],
        ),
        migrations.CreateModel(
            name='MusicArtistToSongRecording',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_created', deform.db.models.fields.fields.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', deform.db.models.fields.fields.DateTimeField(auto_now=True)),
                ('musicartist', deform.db.models.fields.related.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pyamgmt.musicartist')),
            ],
        ),
        migrations.CreateModel(
            name='SongRecording',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_created', deform.db.models.fields.fields.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', deform.db.models.fields.fields.DateTimeField(auto_now=True)),
                ('duration', deform.db.models.fields.fields.DurationField(blank=True, null=True, validators=[pyamgmt.validators.validate_positive_timedelta])),
                ('lyrics', deform.db.models.fields.fields.TextField(blank=True, default='')),
                ('recording_type', deform.db.models.fields.fields.CharField(choices=[('LIVE', 'Live Performance'), ('STUDIO', 'Studio Recording')], default='STUDIO', max_length=6)),
                ('musicartists', deform.db.models.fields.related.ManyToManyField(related_name='_pyamgmt_songrecording_musicartists_+', through='pyamgmt.MusicArtistToSongRecording', to='pyamgmt.MusicArtist')),
                ('song', deform.db.models.fields.related.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pyamgmt.song')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='songversion',
            name='musicartists',
        ),
        migrations.DeleteModel(
            name='MusicArtistToSongVersion',
        ),
        migrations.DeleteModel(
            name='SongVersion',
        ),
        migrations.AddField(
            model_name='musicartisttosongrecording',
            name='songrecording',
            field=deform.db.models.fields.related.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pyamgmt.songrecording'),
        ),
        migrations.AddField(
            model_name='musicalbumtosongrecording',
            name='songrecording',
            field=deform.db.models.fields.related.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pyamgmt.songrecording'),
        ),
        migrations.AddConstraint(
            model_name='musicartisttosongrecording',
            constraint=models.UniqueConstraint(fields=('musicartist', 'songrecording'), name='unique_musicartisttosongrecording'),
        ),
        migrations.AddConstraint(
            model_name='musicalbumtosongrecording',
            constraint=models.UniqueConstraint(fields=('musicalbum', 'songrecording'), name='unique_musicalbumtosongrecording'),
        ),
        migrations.AddConstraint(
            model_name='musicalbumtosongrecording',
            constraint=models.UniqueConstraint(fields=('musicalbum', 'disc_number', 'track_number'), name='unique_musicalbumtosongrecording_disc_track'),
        ),
    ]