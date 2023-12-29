# Generated by Django 5.0 on 2023-12-29 07:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_videogamerole_remove_personxvideogame_role_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MotionPictureXPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name='motionpicturexmusicalbum',
            constraint=models.UniqueConstraint(fields=('motion_picture', 'music_album'), name='unique_motion_picture_x_music_album'),
        ),
        migrations.AddConstraint(
            model_name='motionpicturexsong',
            constraint=models.UniqueConstraint(fields=('motion_picture', 'song'), name='unique_motion_picture_x_song'),
        ),
        migrations.AddField(
            model_name='motionpicturexperson',
            name='motion_picture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='motion_picture_x_person_set', related_query_name='motion_picture_x_person', to='core.motionpicture'),
        ),
        migrations.AddField(
            model_name='motionpicturexperson',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='motion_picture_x_person_set', related_query_name='motion_picture_x_person', to='core.person'),
        ),
        migrations.AddConstraint(
            model_name='motionpicturexperson',
            constraint=models.UniqueConstraint(fields=('motion_picture', 'person'), name='unique_motion_picture_x_person'),
        ),
    ]