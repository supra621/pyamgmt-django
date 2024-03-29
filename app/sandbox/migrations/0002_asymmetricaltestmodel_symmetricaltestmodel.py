# Generated by Django 5.0 on 2023-12-17 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sandbox', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsymmetricalTestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
                ('m2m', models.ManyToManyField(to='sandbox.asymmetricaltestmodel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SymmetricalTestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
                ('m2m', models.ManyToManyField(to='sandbox.symmetricaltestmodel')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
