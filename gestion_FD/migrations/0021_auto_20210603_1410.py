# Generated by Django 3.2.3 on 2021-06-03 13:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_FD', '0020_auto_20210603_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorant',
            name='date_deliberation',
            field=models.DateField(default=datetime.datetime(2021, 6, 3, 14, 10, 13, 101698)),
        ),
        migrations.AlterField(
            model_name='doctorant',
            name='date_inscription',
            field=models.DateField(default=datetime.datetime(2021, 6, 3, 14, 10, 13, 101698)),
        ),
        migrations.AlterField(
            model_name='doctorant',
            name='date_naissance',
            field=models.DateField(default=datetime.datetime(2021, 6, 3, 14, 10, 13, 101698)),
        ),
        migrations.AlterField(
            model_name='doctorant',
            name='date_reinscription',
            field=models.DateField(default=datetime.datetime(2021, 6, 3, 14, 10, 13, 101698)),
        ),
        migrations.AlterField(
            model_name='employe',
            name='date_naissance',
            field=models.DateField(default=datetime.datetime(2021, 6, 3, 14, 10, 13, 98705)),
        ),
        migrations.AlterField(
            model_name='eval_module',
            name='date_eval',
            field=models.DateField(default=datetime.datetime(2021, 6, 3, 14, 10, 13, 106687)),
        ),
        migrations.AlterField(
            model_name='fiche_evaluation',
            name='date_eval',
            field=models.DateField(default=datetime.datetime(2021, 6, 3, 14, 10, 13, 104694)),
        ),
        migrations.AlterField(
            model_name='presentation',
            name='date_pres',
            field=models.DateField(default=datetime.datetime(2021, 6, 3, 14, 10, 13, 103694)),
        ),
        migrations.AlterField(
            model_name='pv',
            name='date_pv',
            field=models.DateField(default=datetime.datetime(2021, 6, 3, 14, 10, 13, 107684)),
        ),
        migrations.AlterField(
            model_name='reinscription',
            name='date_reinscription',
            field=models.DateField(default=datetime.datetime(2021, 6, 3, 14, 10, 13, 100699)),
        ),
    ]
