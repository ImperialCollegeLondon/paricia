# Generated by Django 2.2.1 on 2020-03-27 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('validacion', '0003_auto_20200310_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReporteDiario',
            fields=[
                ('numero_fila', models.BigAutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField()),
                ('valor', models.DecimalField(decimal_places=6, max_digits=14, null=True)),
                ('maximo', models.DecimalField(decimal_places=6, max_digits=14, null=True)),
                ('minimo', models.DecimalField(decimal_places=6, max_digits=14, null=True)),
                ('porcentaje', models.DecimalField(decimal_places=6, max_digits=14, null=True)),
                ('class_valor', models.CharField(max_length=30)),
                ('class_maximo', models.CharField(max_length=30)),
                ('class_minimo', models.CharField(max_length=30)),
                ('class_porcentaje', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ReporteDiarioPrecipitacion',
            fields=[
                ('numero_fila', models.BigAutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField()),
                ('valor', models.DecimalField(decimal_places=6, max_digits=14, null=True)),
                ('porcentaje', models.DecimalField(decimal_places=6, max_digits=14, null=True)),
                ('class_valor', models.CharField(max_length=30)),
                ('class_porcentaje', models.CharField(max_length=30)),
            ],
        ),
    ]