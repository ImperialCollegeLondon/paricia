# Generated by Django 2.2.1 on 2019-09-23 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicion', '0009_auto_20190507_1655'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReporteValidacion',
            fields=[
                ('numero_fila', models.BigAutoField(primary_key=True, serialize=False)),
                ('seleccionado', models.BooleanField()),
                ('fecha', models.DateTimeField()),
                ('valor_seleccionado', models.DecimalField(decimal_places=6, max_digits=14, null=True)),
                ('valor', models.DecimalField(decimal_places=6, max_digits=14, null=True)),
                ('variacion_consecutiva', models.DecimalField(decimal_places=6, max_digits=14, null=True)),
                ('comentario', models.CharField(max_length=350)),
                ('class_fila', models.CharField(max_length=30)),
                ('class_fecha', models.CharField(max_length=30)),
                ('class_validacion', models.CharField(max_length=30)),
                ('class_valor', models.CharField(max_length=30)),
                ('class_variacion_consecutiva', models.CharField(max_length=30)),
                ('class_stddev_error', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='VoltajeBateria',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('estacion', models.PositiveIntegerField(verbose_name='Estacion')),
                ('fecha', models.DateTimeField(verbose_name='Fecha')),
                ('valor', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Valor')),
                ('maximo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Máximo')),
                ('minimo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Mínimo')),
            ],
        ),
        migrations.AddIndex(
            model_name='voltajebateria',
            index=models.Index(fields=['estacion', 'fecha'], name='medicion_vo_estacio_2f4b75_idx'),
        ),
        migrations.AddIndex(
            model_name='voltajebateria',
            index=models.Index(fields=['fecha', 'estacion'], name='medicion_vo_fecha_a1e1e7_idx'),
        ),
    ]