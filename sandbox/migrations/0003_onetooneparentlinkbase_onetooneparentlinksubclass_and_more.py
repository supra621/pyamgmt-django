# Generated by Django 4.0.5 on 2022-08-10 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sandbox', '0002_onetoonetablebase_onetoonetablesubclass_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OneToOneParentLinkBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='OneToOneParentLinkSubclass',
            fields=[
                ('onetooneparentlinkbase', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sandbox.onetooneparentlinkbase')),
                ('subclass_name', models.CharField(max_length=31)),
            ],
        ),
        migrations.AddConstraint(
            model_name='onetooneparentlinksubclass',
            constraint=models.UniqueConstraint(fields=('onetooneparentlinkbase', 'subclass_name'), name='uix_onetooneparentlinksubclass'),
        ),
    ]
