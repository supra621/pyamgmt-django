# Generated by Django 5.0 on 2024-01-06 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_photo_attribution'),
    ]

    operations = [
        migrations.AddField(
            model_name='videogame',
            name='notes',
            field=models.TextField(blank=True),
        ),
    ]
