# Generated by Django 5.0 on 2024-01-07 01:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_rename_comments_musicartist_notes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='beer',
            options={},
        ),
        migrations.AlterModelOptions(
            name='brewery',
            options={'verbose_name_plural': 'breweries'},
        ),
    ]
