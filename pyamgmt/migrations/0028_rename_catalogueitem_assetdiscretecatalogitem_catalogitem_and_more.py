# Generated by Django 4.0 on 2021-12-28 22:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pyamgmt', '0027_rename_invoicelineitemtononcatalogueitem_invoicelineitemtononcatalogitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assetdiscretecatalogitem',
            old_name='catalogueitem',
            new_name='catalogitem',
        ),
        migrations.RenameField(
            model_name='assetinventory',
            old_name='catalogueitem',
            new_name='catalogitem',
        ),
        migrations.RenameField(
            model_name='catalogitemdigitalsong',
            old_name='catalogueitem',
            new_name='catalogitem',
        ),
        migrations.RenameField(
            model_name='catalogitemmusicalbum',
            old_name='catalogueitem',
            new_name='catalogitem',
        ),
        migrations.RenameField(
            model_name='catalogitemtoinvoicelineitem',
            old_name='catalogueitem',
            new_name='catalogitem',
        ),
        migrations.RenameField(
            model_name='catalogitemtoorderlineitem',
            old_name='catalogueitem',
            new_name='catalogitem',
        ),
        migrations.RenameField(
            model_name='catalogitemtopointofsalelineitem',
            old_name='catalogueitem',
            new_name='catalogitem',
        ),
        migrations.RenameField(
            model_name='invoicelineitemtononcatalogitem',
            old_name='noncatalogueitem',
            new_name='noncatalogitem',
        ),
    ]