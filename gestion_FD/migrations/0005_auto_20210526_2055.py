# Generated by Django 3.2.3 on 2021-05-26 19:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_FD', '0004_auto_20210525_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorant',
            name='date_deliberation',
            field=models.DateField(default=datetime.datetime(2021, 5, 26, 20, 55, 34, 476278)),
        ),
        migrations.AlterField(
            model_name='doctorant',
            name='date_inscription',
            field=models.DateField(default=datetime.datetime(2021, 5, 26, 20, 55, 34, 476278)),
        ),
        migrations.AlterField(
            model_name='doctorant',
            name='date_naissance',
            field=models.DateField(default=datetime.datetime(2021, 5, 26, 20, 55, 34, 476278)),
        ),
        migrations.AlterField(
            model_name='doctorant',
            name='date_reinscription',
            field=models.DateField(default=datetime.datetime(2021, 5, 26, 20, 55, 34, 476278)),
        ),
        migrations.AlterField(
            model_name='employe',
            name='date_naissance',
            field=models.DateField(default=datetime.datetime(2021, 5, 26, 20, 55, 34, 477276)),
        ),
        migrations.AlterField(
            model_name='eval_module',
            name='date_eval',
            field=models.DateField(default=datetime.datetime(2021, 5, 26, 20, 55, 34, 480268)),
        ),
        migrations.AlterField(
            model_name='fiche_evaluation',
            name='date_eval',
            field=models.DateField(default=datetime.datetime(2021, 5, 26, 20, 55, 34, 479271)),
        ),
        migrations.AlterField(
            model_name='piecejointe',
            name='lien',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='pv',
            name='date_pv',
            field=models.DateField(default=datetime.datetime(2021, 5, 26, 20, 55, 34, 482262)),
        ),
    ]
