# Generated by Django 5.0 on 2024-01-09 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_beerxuser_beerxuser_unique_beer_x_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='beerxuser',
            options={'verbose_name': 'Beer <-> User', 'verbose_name_plural': 'Beer <-> User'},
        ),
        migrations.RenameField(
            model_name='beerxuser',
            old_name='approval',
            new_name='approved',
        ),
    ]
