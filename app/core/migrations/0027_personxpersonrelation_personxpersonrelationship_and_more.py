# Generated by Django 5.0 on 2023-12-27 03:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_delete_personxperson'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonXPersonRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('relation', models.CharField(choices=[('BROTHER', 'Brother'), ('CHILD', 'Child'), ('DAUGHTER', 'Daughter'), ('FATHER', 'Father'), ('FRIEND', 'Friend'), ('GRANDCHILD', 'Grandchild'), ('GRANDDAUGHTER', 'Granddaughter'), ('GRANDFATHER', 'Grandfather'), ('GRANDMOTHER', 'Grandmother'), ('GRANDPARENT', 'Grandparent'), ('GRANDSON', 'Grandson'), ('MOTHER', 'Mother'), ('SIBLING', 'Sibling'), ('SISTER', 'Sister'), ('SON', 'Son')], help_text="Relation FROM Person A TO Person B. Person A is Person B's ...", max_length=13)),
                ('person_a', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.person')),
                ('person_b', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.person')),
            ],
        ),
        migrations.CreateModel(
            name='PersonXPersonRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('relationship', models.CharField(blank=True, choices=[('HUSBAND', 'Husband'), ('PARTNER', 'Partner'), ('SPOUSE', 'Spouse'), ('WIFE', 'Wife')], help_text="The relationship FROM person A TO person B. Person A is Person B's ...", max_length=7)),
                ('person_a', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.person')),
                ('person_b', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.person')),
            ],
        ),
        migrations.CreateModel(
            name='PersonXPersonRelationshipActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('from_year', models.PositiveSmallIntegerField()),
                ('until_year', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('person_x_person_relationship', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='person_x_person_relationship_activity_set', related_query_name='person_x_person_relationship_activity', to='core.personxpersonrelationship')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='personxpersonrelation',
            constraint=models.UniqueConstraint(fields=('person_a', 'person_b'), name='unique_person_x_person_relation'),
        ),
        migrations.AddConstraint(
            model_name='personxpersonrelation',
            constraint=models.CheckConstraint(check=models.Q(('person_a', models.F('person_b')), _negated=True), name='person_x_person_relation_not_self'),
        ),
        migrations.AddConstraint(
            model_name='personxpersonrelationship',
            constraint=models.UniqueConstraint(fields=('person_a', 'person_b'), name='unique_person_x_person_relationship'),
        ),
        migrations.AddConstraint(
            model_name='personxpersonrelationship',
            constraint=models.CheckConstraint(check=models.Q(('person_a', models.F('person_b')), _negated=True), name='person_x_person_relationship_not_self'),
        ),
    ]
