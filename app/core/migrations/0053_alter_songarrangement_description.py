# Generated by Django 5.0 on 2023-12-20 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0052_songrecording_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='songarrangement',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
