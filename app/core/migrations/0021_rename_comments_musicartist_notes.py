# Generated by Django 5.0 on 2024-01-06 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_videogame_notes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='musicartist',
            old_name='comments',
            new_name='notes',
        ),
    ]
