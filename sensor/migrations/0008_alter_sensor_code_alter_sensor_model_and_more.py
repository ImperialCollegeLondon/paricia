# Generated by Django 5.1 on 2024-09-11 04:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0007_alter_sensor_owner_alter_sensor_visibility_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='code',
            field=models.CharField(help_text='Sensor code.', max_length=32, unique=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='model',
            field=models.CharField(blank=True, help_text='Specific model of the sensor.', max_length=150, null=True, verbose_name='Model'),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='sensor_brand',
            field=models.ForeignKey(help_text='Sensor brand.', null=True, on_delete=django.db.models.deletion.PROTECT, to='sensor.sensorbrand', verbose_name='Sensor brand'),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='sensor_id',
            field=models.AutoField(help_text='Primary key.', primary_key=True, serialize=False, verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='sensor_type',
            field=models.ForeignKey(help_text='Sensor type.', on_delete=django.db.models.deletion.PROTECT, to='sensor.sensortype', verbose_name='Sensor type'),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='serial',
            field=models.CharField(blank=True, help_text='Serial number of the sensor.', max_length=20, null=True, verbose_name='Serial number'),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='status',
            field=models.BooleanField(default=False, help_text='If the sensor is active.', verbose_name='Status (active)'),
        ),
        migrations.AlterField(
            model_name='sensorbrand',
            name='brand_id',
            field=models.AutoField(help_text='Primary key', primary_key=True, serialize=False, verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='sensorbrand',
            name='name',
            field=models.CharField(help_text='Name of the brand.', max_length=25, verbose_name='Brand name'),
        ),
        migrations.AlterField(
            model_name='sensortype',
            name='name',
            field=models.CharField(help_text='Sensor type name.', max_length=25, verbose_name='Sensor type'),
        ),
        migrations.AlterField(
            model_name='sensortype',
            name='type_id',
            field=models.AutoField(help_text='Primary key.', primary_key=True, serialize=False, verbose_name='Id'),
        ),
    ]
