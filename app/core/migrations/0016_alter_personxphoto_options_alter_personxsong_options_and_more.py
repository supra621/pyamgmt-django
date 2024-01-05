# Generated by Django 5.0 on 2024-01-05 06:42

import django_base.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_alter_account_options_alter_accountasset_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='personxphoto',
            options={'verbose_name': 'Person <-> Photo', 'verbose_name_plural': 'Person <-> Photo'},
        ),
        migrations.AlterModelOptions(
            name='personxsong',
            options={'verbose_name': 'Person <-> Song', 'verbose_name_plural': 'Person <-> Song'},
        ),
        migrations.AlterModelOptions(
            name='personxsongarrangement',
            options={'verbose_name': 'Person <-> SongArrangement', 'verbose_name_plural': 'Person <-> SongArrangement'},
        ),
        migrations.AlterModelOptions(
            name='personxsongperformance',
            options={'verbose_name': 'Person <-> SongPerformance', 'verbose_name_plural': 'Person <-> SongPerformance'},
        ),
        migrations.AlterModelOptions(
            name='personxvideogame',
            options={'verbose_name': 'Person <-> VideoGame', 'verbose_name_plural': 'Person <-> VideoGame'},
        ),
        migrations.AlterModelOptions(
            name='personxvideogamexvideogamerole',
            options={'verbose_name': 'Person <-> VideoGame <-> VideoGameRole', 'verbose_name_plural': 'Person <-> VideoGame <-> VideoGameRole'},
        ),
        migrations.AddField(
            model_name='videogame',
            name='year_published',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django_base.validators.validate_year_not_future]),
        ),
        migrations.AlterField(
            model_name='videogameaddon',
            name='release_date',
            field=models.DateField(blank=True, null=True, validators=[django_base.validators.validate_date_not_future]),
        ),
        migrations.AlterField(
            model_name='videogameedition',
            name='release_date',
            field=models.DateField(blank=True, null=True, validators=[django_base.validators.validate_date_not_future]),
        ),
        migrations.AlterField(
            model_name='videogameeditionxvideogameplatform',
            name='release_date',
            field=models.DateField(blank=True, null=True, validators=[django_base.validators.validate_date_not_future]),
        ),
        migrations.AlterField(
            model_name='videogameplatformregion',
            name='release_date',
            field=models.DateField(blank=True, null=True, validators=[django_base.validators.validate_date_not_future]),
        ),
        migrations.AddConstraint(
            model_name='videogameeditionxvideogameplatform',
            constraint=models.UniqueConstraint(fields=('video_game_edition', 'video_game_platform'), name='unique_video_game_edition_x_video_game_platform'),
        ),
    ]
