# Generated by Django 4.0.5 on 2022-06-27 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyamgmt', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='booktomotionpicture',
            constraint=models.UniqueConstraint(fields=('book', 'motionpicture'), name='unique_booktomotionpicture'),
        ),
    ]
