# Generated by Django 4.0 on 2022-01-04 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pyamgmt', '0030_alter_catalogitem_isbn_13'),
    ]

    operations = [
        migrations.RenameField(
            model_name='catalogitem',
            old_name='upc',
            new_name='upc_a',
        ),
    ]