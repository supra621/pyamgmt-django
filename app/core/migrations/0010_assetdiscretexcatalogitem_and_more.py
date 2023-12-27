# Generated by Django 5.0 on 2023-12-24 03:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_catalogitemdigitalsong_song_recording'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetDiscreteXCatalogItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('asset_discrete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asset_discrete_x_catalog_item_set', related_query_name='asset_discrete_x_catalog_item', to='core.assetdiscrete')),
                ('catalog_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asset_discrete_x_catalog_item_set', related_query_name='asset_discrete_x_catalog_item', to='core.catalogitem')),
            ],
            options={
                'verbose_name': 'Asset::Discrete::CatalogItem',
                'verbose_name_plural': 'Asset::Discrete::CatalogItem',
            },
        ),
        migrations.DeleteModel(
            name='AssetDiscreteCatalogItem',
        ),
    ]