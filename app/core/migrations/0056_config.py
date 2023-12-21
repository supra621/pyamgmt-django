# Generated by Django 5.0 on 2023-12-21 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0055_remove_song_is_original'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('key', models.CharField(choices=[('ROOT_HEADER_TEXT', 'Root Header Text')], max_length=16, primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
