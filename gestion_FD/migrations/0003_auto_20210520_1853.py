# Generated by Django 3.2.3 on 2021-05-20 17:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_FD', '0002_auto_20210520_1834'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Compte',
        ),
        migrations.AlterField(
            model_name='doctorant',
            name='date_deliberation',
            field=models.DateField(default=datetime.datetime(2021, 5, 20, 18, 53, 28, 672919)),
        ),
        migrations.AlterField(
            model_name='doctorant',
            name='date_inscription',
            field=models.DateField(default=datetime.datetime(2021, 5, 20, 18, 53, 28, 672919)),
        ),
        migrations.AlterField(
            model_name='doctorant',
            name='date_naissance',
            field=models.DateField(default=datetime.datetime(2021, 5, 20, 18, 53, 28, 672919)),
        ),
        migrations.AlterField(
            model_name='doctorant',
            name='date_reinscription',
            field=models.DateField(default=datetime.datetime(2021, 5, 20, 18, 53, 28, 672919)),
        ),
        migrations.AlterField(
            model_name='employe',
            name='date_naissance',
            field=models.DateField(default=datetime.datetime(2021, 5, 20, 18, 53, 28, 672919)),
        ),
        migrations.AlterField(
            model_name='eval_module',
            name='date_eval',
            field=models.DateField(default=datetime.datetime(2021, 5, 20, 18, 53, 28, 688543)),
        ),
        migrations.AlterField(
            model_name='fiche_evaluation',
            name='date_eval',
            field=models.DateField(default=datetime.datetime(2021, 5, 20, 18, 53, 28, 688543)),
        ),
        migrations.AlterField(
            model_name='pv',
            name='date_pv',
            field=models.DateField(default=datetime.datetime(2021, 5, 20, 18, 53, 28, 688543)),
        ),
    ]
