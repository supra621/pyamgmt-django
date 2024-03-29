# Generated by Django 5.0 on 2024-01-04 06:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_delete_assetdiscretexcatalogitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetdiscrete',
            name='subtype',
            field=models.CharField(choices=[('CATALOG_ITEM', 'CATALOG_ITEM'), ('MANUFACTURED', 'MANUFACTURED'), ('VEHICLE', 'VEHICLE')], default='NONE', max_length=31),
        ),
        migrations.CreateModel(
            name='AssetDiscreteXCatalogItem',
            fields=[
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('asset_discrete', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='asset_discrete_x_catalog_item', serialize=False, to='core.assetdiscrete')),
                ('catalog_item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='asset_discrete_x_catalog_item_set', related_query_name='asset_discrete_x_catalog_item', to='core.catalogitem')),
            ],
            options={
                'verbose_name': 'Asset::Discrete::CatalogItem',
                'verbose_name_plural': 'Asset::Discrete::CatalogItem',
            },
        ),
        migrations.CreateModel(
            name='CatalogItemManufactured',
            fields=[
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('catalog_item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='catalog_item_manufactured', serialize=False, to='core.catalogitem')),
                ('part_number', models.CharField(blank=True, max_length=255)),
                ('manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='catalog_item_manufactured_set', related_query_name='catalog_item_manufactured', to='core.manufacturer')),
            ],
        ),
        migrations.AddConstraint(
            model_name='catalogitemmanufactured',
            constraint=models.UniqueConstraint(fields=('manufacturer', 'part_number'), name='unique_catalog_item_manufactured'),
        ),
    ]
