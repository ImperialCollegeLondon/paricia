# Generated by Django 5.1 on 2024-09-11 13:02

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0012_alter_measurement_station_alter_report_station'),
        ('station', '0015_remove_deltat_station_station_delta_t_and_more'),
        ('variable', '0009_remove_variable_diff_warning_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='depth',
            field=models.PositiveSmallIntegerField(blank=True, help_text='Depth of the measurement.', null=True, verbose_name='depth'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='direction',
            field=models.DecimalField(blank=True, decimal_places=6, help_text='Direction of the measurement, useful for vector quantities. It should be a number in the [0, 360) interval, where 0 represents north.', max_digits=14, null=True, verbose_name='direction'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Flag to indicate if the measurement is active. An inactive measurement is not used for reporting.', verbose_name='Active?'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='is_validated',
            field=models.BooleanField(default=False, help_text='Flag to indicate if the measurement has been validated.', verbose_name='Validated?'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='maximum',
            field=models.DecimalField(blank=True, decimal_places=6, help_text='Maximum value of the measurement. Mostly useful for reports or when the measurement represents an average over time.', max_digits=14, null=True, verbose_name='maximum'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='minimum',
            field=models.DecimalField(blank=True, decimal_places=6, help_text='Minimum value of the measurement. Mostly useful for reports or when the measurement represents an average over time.', max_digits=14, null=True, verbose_name='minimum'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='raw_depth',
            field=models.PositiveSmallIntegerField(blank=True, editable=False, help_text='Original depth of the measurement.', null=True, verbose_name='raw depth'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='raw_direction',
            field=models.DecimalField(blank=True, decimal_places=6, editable=False, help_text='Original direction of the measurement.', max_digits=14, null=True, verbose_name='raw direction'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='raw_maximum',
            field=models.DecimalField(blank=True, decimal_places=6, editable=False, help_text='Original maximum value of the measurement.', max_digits=14, null=True, verbose_name='raw maximum'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='raw_minimum',
            field=models.DecimalField(blank=True, decimal_places=6, editable=False, help_text='Original minimum value of the measurement.', max_digits=14, null=True, verbose_name='raw minimum'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='raw_value',
            field=models.DecimalField(blank=True, decimal_places=6, editable=False, help_text='Original value of the measurement.', max_digits=14, null=True, verbose_name='raw value'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='station',
            field=models.ForeignKey(help_text='Station this measurement belongs to.', on_delete=django.db.models.deletion.PROTECT, to='station.station', verbose_name='Station'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='value',
            field=models.DecimalField(decimal_places=6, help_text='Value of the measurement.', max_digits=14, verbose_name='value'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='variable',
            field=models.ForeignKey(help_text='Variable being measured.', on_delete=django.db.models.deletion.PROTECT, to='variable.variable', verbose_name='Variable'),
        ),
        migrations.AlterField(
            model_name='report',
            name='completeness',
            field=models.DecimalField(decimal_places=1, help_text='Completeness of the report. Eg. a daily report made out of 24 hourly measurements would have a completeness of 100%.', max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='report',
            name='maximum',
            field=models.DecimalField(blank=True, decimal_places=6, help_text='Maximum value of the measurement. Mostly useful for reports or when the measurement represents an average over time.', max_digits=14, null=True, verbose_name='maximum'),
        ),
        migrations.AlterField(
            model_name='report',
            name='minimum',
            field=models.DecimalField(blank=True, decimal_places=6, help_text='Minimum value of the measurement. Mostly useful for reports or when the measurement represents an average over time.', max_digits=14, null=True, verbose_name='minimum'),
        ),
        migrations.AlterField(
            model_name='report',
            name='report_type',
            field=models.CharField(choices=[('hourly', 'Hourly'), ('daily', 'Daily'), ('monthly', 'Montly')], help_text='Type of report. It can be hourly, daily or monthly.', max_length=7),
        ),
        migrations.AlterField(
            model_name='report',
            name='station',
            field=models.ForeignKey(help_text='Station this measurement belongs to.', on_delete=django.db.models.deletion.PROTECT, to='station.station', verbose_name='Station'),
        ),
        migrations.AlterField(
            model_name='report',
            name='value',
            field=models.DecimalField(decimal_places=6, help_text='Value of the measurement.', max_digits=14, verbose_name='value'),
        ),
        migrations.AlterField(
            model_name='report',
            name='variable',
            field=models.ForeignKey(help_text='Variable being measured.', on_delete=django.db.models.deletion.PROTECT, to='variable.variable', verbose_name='Variable'),
        ),
    ]