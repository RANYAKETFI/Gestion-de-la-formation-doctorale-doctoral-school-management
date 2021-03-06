# Generated by Django 3.2.3 on 2021-06-04 16:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_FD', '0025_auto_20210604_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorant',
            name='rein_envo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='doctorant',
            name='date_deliberation',
            field=models.DateField(default=datetime.datetime(2021, 6, 4, 17, 28, 7, 853360)),
        ),
        migrations.AlterField(
            model_name='doctorant',
            name='date_inscription',
            field=models.DateField(default=datetime.datetime(2021, 6, 4, 17, 28, 7, 853360)),
        ),
        migrations.AlterField(
            model_name='doctorant',
            name='date_naissance',
            field=models.DateField(default=datetime.datetime(2021, 6, 4, 17, 28, 7, 853360)),
        ),
        migrations.AlterField(
            model_name='doctorant',
            name='date_reinscription',
            field=models.DateField(default=datetime.datetime(2021, 6, 4, 17, 28, 7, 853360)),
        ),
        migrations.AlterField(
            model_name='employe',
            name='date_naissance',
            field=models.DateField(default=datetime.datetime(2021, 6, 4, 17, 28, 7, 850368)),
        ),
        migrations.AlterField(
            model_name='eval_module',
            name='date_eval',
            field=models.DateField(default=datetime.datetime(2021, 6, 4, 17, 28, 7, 859344)),
        ),
        migrations.AlterField(
            model_name='fiche_evaluation',
            name='date_eval',
            field=models.DateField(default=datetime.datetime(2021, 6, 4, 17, 28, 7, 857349)),
        ),
        migrations.AlterField(
            model_name='presentation',
            name='date_pres',
            field=models.DateField(default=datetime.datetime(2021, 6, 4, 17, 28, 7, 856352)),
        ),
        migrations.AlterField(
            model_name='pv',
            name='date_pv',
            field=models.DateField(default=datetime.datetime(2021, 6, 4, 17, 28, 7, 859344)),
        ),
        migrations.AlterField(
            model_name='reinscription',
            name='date_reinscription',
            field=models.DateField(default=datetime.datetime(2021, 6, 4, 17, 28, 7, 852363)),
        ),
    ]
