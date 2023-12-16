# Generated by Django 5.0 on 2023-12-16 04:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_catalogitemxvideogameplatformedition_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('document', models.FileField(upload_to='')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_document_set', related_query_name='invoice_document', to='core.invoice')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InvoiceXTxn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.invoice')),
                ('txn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.txn')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='PointOfSaleXTxn',
        ),
    ]
