# Generated by Django 5.1 on 2024-09-06 09:14

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0007_alter_sensor_owner_alter_sensor_visibility_and_more'),
        ('station', '0014_alter_station_timezone'),
        ('variable', '0007_alter_sensorinstallation_owner_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variable',
            name='automatic_report',
        ),
        migrations.RemoveField(
            model_name='variable',
            name='is_active',
        ),
        migrations.AlterField(
            model_name='sensorinstallation',
            name='end_date',
            field=models.DateField(blank=True, help_text='End date of the installation', null=True, verbose_name='End date'),
        ),
        migrations.AlterField(
            model_name='sensorinstallation',
            name='sensor',
            field=models.ForeignKey(help_text='Sensor used for the measurement.', on_delete=django.db.models.deletion.PROTECT, to='sensor.sensor', verbose_name='Sensor'),
        ),
        migrations.AlterField(
            model_name='sensorinstallation',
            name='sensorinstallation_id',
            field=models.AutoField(help_text='Primary key.', primary_key=True, serialize=False, verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='sensorinstallation',
            name='start_date',
            field=models.DateField(help_text='Start date of the installation', verbose_name='Start date'),
        ),
        migrations.AlterField(
            model_name='sensorinstallation',
            name='state',
            field=models.BooleanField(default=True, help_text='Is the sensor active?', verbose_name='Is active?'),
        ),
        migrations.AlterField(
            model_name='sensorinstallation',
            name='station',
            field=models.ForeignKey(help_text='Station where the sensor is installed.', on_delete=django.db.models.deletion.PROTECT, to='station.station', verbose_name='Station'),
        ),
        migrations.AlterField(
            model_name='sensorinstallation',
            name='variable',
            field=models.ForeignKey(help_text='Variable measured by the sensor.', on_delete=django.db.models.deletion.PROTECT, to='variable.variable', verbose_name='Variable'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='initials',
            field=models.CharField(help_text='Symbol for the unit, eg. m/s.', max_length=10, verbose_name='Symbol'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='name',
            field=models.CharField(help_text='Name of the unit, eg. meters per second.', max_length=50, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='unit_id',
            field=models.AutoField(help_text='Primary key.', primary_key=True, serialize=False, verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='variable',
            name='diff_error',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='If two sequential values in the time-series data of this variable differ by more than this value, the validation process can mark this with an error flag.', max_digits=7, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Difference error'),
        ),
        migrations.AlterField(
            model_name='variable',
            name='diff_warning',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='If two sequential values in the time-series data of this variable differ by more than this value, the validation process can mark this with a warning flag.', max_digits=7, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Difference warning'),
        ),
        migrations.AlterField(
            model_name='variable',
            name='maximum',
            field=models.DecimalField(decimal_places=2, help_text='Maximum value allowed for the variable.', max_digits=7, verbose_name='Maximum'),
        ),
        migrations.AlterField(
            model_name='variable',
            name='minimum',
            field=models.DecimalField(decimal_places=2, help_text='Minimum value allowed for the variable.', max_digits=7, verbose_name='Minimum'),
        ),
        migrations.AlterField(
            model_name='variable',
            name='name',
            field=models.CharField(help_text='Human-readable name of the variable, eg. Air temperature.', max_length=50, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='variable',
            name='nature',
            field=models.CharField(choices=[('sum', 'sum'), ('average', 'average'), ('value', 'value')], default='value', help_text='Nature of the variable, eg. if it represents a one-off magnitude, the average over a period of time or the cumulative value over a period of time.', max_length=10, verbose_name='Nature of the measurement'),
        ),
        migrations.AlterField(
            model_name='variable',
            name='null_limit',
            field=models.DecimalField(decimal_places=1, default=0, help_text='The max \\% of null values (missing, caused by e.g. equipment malfunction) allowed for hourly, daily, monthly data. Cumulative values are not deemed trustworthy if the number of missing values in a given period is greater than the null_limit.', max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Null limit (%)'),
        ),
        migrations.AlterField(
            model_name='variable',
            name='outlier_limit',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='How many times the standard deviation (sigma) is considered an outlier for this variable.', max_digits=7, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Sigmas (outliers)'),
        ),
        migrations.AlterField(
            model_name='variable',
            name='unit',
            field=models.ForeignKey(blank=True, help_text='Unit of the variable.', null=True, on_delete=django.db.models.deletion.PROTECT, to='variable.unit', verbose_name='Unit'),
        ),
        migrations.AlterField(
            model_name='variable',
            name='variable_code',
            field=models.CharField(help_text='Code of the variable, eg. airtemperature.', max_length=100, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='variable',
            name='variable_id',
            field=models.AutoField(help_text='Primary key.', primary_key=True, serialize=False, verbose_name='Id'),
        ),
    ]