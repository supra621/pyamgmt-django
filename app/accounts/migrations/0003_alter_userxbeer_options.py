# Generated by Django 5.0 on 2024-01-10 03:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userxbeer_userxbeer_unique_user_x_beer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userxbeer',
            options={'verbose_name': 'User <-> Beer', 'verbose_name_plural': 'Users <-> Beer'},
        ),
    ]