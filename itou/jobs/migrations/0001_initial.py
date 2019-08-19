# Generated by Django 2.2.4 on 2019-08-19 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rome',
            fields=[
                ('code', models.CharField(max_length=5, primary_key=True, serialize=False, verbose_name='Code ROME')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Nom')),
                ('riasec_major', models.CharField(choices=[('R', 'Réaliste'), ('I', 'Investigateur'), ('A', 'Artistique'), ('S', 'Social'), ('E', 'Entreprenant'), ('C', 'Conventionnel')], default='R', max_length=1, verbose_name='RIASEC Majeur')),
                ('riasec_minor', models.CharField(choices=[('R', 'Réaliste'), ('I', 'Investigateur'), ('A', 'Artistique'), ('S', 'Social'), ('E', 'Entreprenant'), ('C', 'Conventionnel')], default='R', max_length=1, verbose_name='RIASEC Mineur')),
                ('code_isco', models.CharField(max_length=4, verbose_name='Code ROME')),
            ],
            options={
                'verbose_name': 'Métier',
                'verbose_name_plural': 'Métiers',
            },
        ),
        migrations.CreateModel(
            name='Appellation',
            fields=[
                ('code', models.CharField(max_length=6, primary_key=True, serialize=False, verbose_name='Code')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Nom')),
                ('short_name', models.CharField(db_index=True, max_length=255, verbose_name='Nom court')),
                ('rome', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appellations', to='jobs.Rome')),
            ],
            options={
                'verbose_name': 'Appellation',
                'verbose_name_plural': 'Appellations',
                'ordering': ['short_name', 'name'],
            },
        ),
    ]
