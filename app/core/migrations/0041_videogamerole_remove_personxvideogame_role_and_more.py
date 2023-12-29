# Generated by Django 5.0 on 2023-12-29 05:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_videogame_personnel'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoGameRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='personxvideogame',
            name='role',
        ),
        migrations.CreateModel(
            name='PersonXVideoGameXVideoGameRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('person_x_video_game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_x_video_game_x_video_game_role_set', related_query_name='person_x_video_game_x_video_game_role', to='core.personxvideogame')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='person_x_video_game_x_video_game_role_set', related_query_name='person_x_video_game_x_video_game_role', to='core.videogamerole')),
            ],
        ),
        migrations.AddConstraint(
            model_name='personxvideogamexvideogamerole',
            constraint=models.UniqueConstraint(fields=('person_x_video_game', 'role'), name='unique_person_x_video_game_x_video_game_role'),
        ),
    ]