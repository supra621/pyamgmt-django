# Generated by Django 3.2.6 on 2021-09-17 16:26

import deform.db.models.fields.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pyamgmt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='lyrics',
            field=deform.db.models.fields.fields.TextField(blank=True, null=True),
        ),
    ]
