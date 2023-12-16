# Generated by Django 5.0 on 2023-12-16 02:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_asset_account_asset_real'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalogitemmusicalbumproduction',
            name='media_format',
        ),
        migrations.AddField(
            model_name='catalogitemmusicalbumproduction',
            name='music_album_production',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='catalog_item_music_album_production_set', related_query_name='catalog_item_music_album_production', to='core.musicalbumproduction'),
        ),
    ]
