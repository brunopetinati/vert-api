# Generated by Django 4.1.7 on 2023-03-07 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='federal_debt',
        ),
        migrations.RemoveField(
            model_name='project',
            name='has_car',
        ),
        migrations.RemoveField(
            model_name='project',
            name='has_georeferencing_file',
        ),
        migrations.RemoveField(
            model_name='project',
            name='has_matricula_certificate',
        ),
        migrations.RemoveField(
            model_name='project',
            name='has_reserve_legal_deficit',
        ),
        migrations.RemoveField(
            model_name='project',
            name='has_updated_ccir',
        ),
        migrations.AlterField(
            model_name='project',
            name='status_car',
            field=models.CharField(max_length=50),
        ),
    ]
