# Generated by Django 5.0 on 2024-01-09 09:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_assetdiscretemanufactured_assetdiscreterealestate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountassetreal',
            name='asset_discrete',
        ),
        migrations.CreateModel(
            name='AccountAssetRealXAssetDiscrete',
            fields=[
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('asset_discrete', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='account_asset_real_x_asset_discrete', serialize=False, to='core.assetdiscrete')),
                ('account_asset_real', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_asset_real_x_asset_discrete_set', related_query_name='account_asset_real_x_asset_discrete', to='core.accountasset')),
            ],
            options={
                'verbose_name': 'Account::Asset::Real <-> Asset::Discrete',
                'verbose_name_plural': 'Account::Asset::Real <-> Asset::Discrete',
            },
        ),
    ]
