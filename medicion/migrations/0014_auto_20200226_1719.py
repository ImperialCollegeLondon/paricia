# Generated by Django 2.2.1 on 2020-02-26 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicion', '0013_auto_20200226_1045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caudal',
            name='estacion',
        ),
        migrations.RemoveField(
            model_name='direccionviento',
            name='estacion',
        ),
        migrations.RemoveField(
            model_name='humedadaire',
            name='estacion',
        ),
        migrations.RemoveField(
            model_name='humedadsuelo',
            name='estacion',
        ),
        migrations.RemoveField(
            model_name='nivelagua',
            name='estacion',
        ),
        migrations.RemoveField(
            model_name='precipitacion',
            name='estacion',
        ),
        migrations.RemoveField(
            model_name='presionatmosferica',
            name='estacion',
        ),
        migrations.RemoveField(
            model_name='radiacionsolar',
            name='estacion',
        ),
        migrations.RemoveField(
            model_name='temperaturaagua',
            name='estacion',
        ),
        migrations.RemoveField(
            model_name='temperaturaaire',
            name='estacion',
        ),
        migrations.RemoveField(
            model_name='velocidadviento',
            name='estacion',
        ),
        migrations.RemoveField(
            model_name='viento',
            name='estacion',
        ),
        migrations.RemoveField(
            model_name='voltajebateria',
            name='estacion',
        ),
    ]