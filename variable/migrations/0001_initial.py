# Generated by Django 3.0.11 on 2022-07-20 12:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("sensor", "0001_initial"),
        ("station", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Unit",
            fields=[
                (
                    "unit_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="Id"
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Name")),
                ("initials", models.CharField(max_length=10, verbose_name="Initials")),
            ],
            options={
                "ordering": ["unit_id"],
            },
        ),
        migrations.CreateModel(
            name="Variable",
            fields=[
                (
                    "variable_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="Id"
                    ),
                ),
                (
                    "variable_code",
                    models.CharField(max_length=100, verbose_name="Code"),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Name")),
                (
                    "maximum",
                    models.DecimalField(
                        decimal_places=2, max_digits=7, verbose_name="Maximum"
                    ),
                ),
                (
                    "minimum",
                    models.DecimalField(
                        decimal_places=2, max_digits=7, verbose_name="Minimum"
                    ),
                ),
                (
                    "diff_warning",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=7,
                        null=True,
                        verbose_name="Difference warning",
                    ),
                ),
                (
                    "diff_error",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=7,
                        null=True,
                        verbose_name="Difference error",
                    ),
                ),
                (
                    "outlier_limit",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=7,
                        null=True,
                        verbose_name="Sigmas (outliers)",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Active")),
                (
                    "is_cumulative",
                    models.BooleanField(
                        default=True,
                        verbose_name="Cumulative (True) or Averaged (False)",
                    ),
                ),
                (
                    "automatic_report",
                    models.BooleanField(default=True, verbose_name="Automatic report"),
                ),
                (
                    "null_limit",
                    models.DecimalField(
                        decimal_places=1,
                        max_digits=4,
                        null=True,
                        verbose_name="Null limit (%)",
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="variable.Unit",
                        verbose_name="Unit",
                    ),
                ),
            ],
            options={
                "ordering": ["variable_id"],
            },
        ),
        migrations.CreateModel(
            name="SensorInstallation",
            fields=[
                (
                    "sensorinstallation_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="Id"
                    ),
                ),
                ("start_date", models.DateField(verbose_name="Start date")),
                (
                    "end_date",
                    models.DateField(blank=True, null=True, verbose_name="End date"),
                ),
                ("state", models.BooleanField(default=True, verbose_name="Active")),
                (
                    "sensor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="sensor.Sensor",
                        verbose_name="Sensor",
                    ),
                ),
                (
                    "station",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="station.Station",
                        verbose_name="Station",
                    ),
                ),
                (
                    "variable",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="variable.Variable",
                        verbose_name="Variable",
                    ),
                ),
            ],
            options={
                "ordering": ["station"],
            },
        ),
    ]