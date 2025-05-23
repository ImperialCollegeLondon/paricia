# Generated by Django 3.2.14 on 2023-04-15 03:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("variable", "0001_initial"),
        ("station", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Date",
            fields=[
                (
                    "date_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="Id"
                    ),
                ),
                ("date_format", models.CharField(max_length=20, verbose_name="Format")),
                ("code", models.CharField(max_length=20, verbose_name="Code")),
            ],
            options={
                "ordering": ("date_id",),
            },
        ),
        migrations.CreateModel(
            name="Delimiter",
            fields=[
                (
                    "delimiter_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="Id"
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Name")),
                (
                    "character",
                    models.CharField(
                        blank=True, max_length=10, verbose_name="Character"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Extension",
            fields=[
                (
                    "extension_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="Id"
                    ),
                ),
                ("value", models.CharField(max_length=5, verbose_name="Value")),
            ],
        ),
        migrations.CreateModel(
            name="Time",
            fields=[
                (
                    "time_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="Id"
                    ),
                ),
                ("time_format", models.CharField(max_length=20, verbose_name="Format")),
                ("code", models.CharField(max_length=20, verbose_name="Code")),
            ],
            options={
                "ordering": ("time_id",),
            },
        ),
        migrations.CreateModel(
            name="Format",
            fields=[
                (
                    "format_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="format_id"
                    ),
                ),
                ("name", models.CharField(max_length=35, verbose_name="Format name")),
                (
                    "description",
                    models.TextField(null=True, verbose_name="Description"),
                ),
                (
                    "location",
                    models.CharField(
                        blank=True, max_length=300, null=True, verbose_name="Location"
                    ),
                ),
                (
                    "file",
                    models.CharField(
                        blank=True,
                        help_text="Only applies to automatic transmission",
                        max_length=100,
                        null=True,
                        verbose_name="Archivo",
                    ),
                ),
                ("first_row", models.SmallIntegerField(verbose_name="First row")),
                (
                    "footer_rows",
                    models.SmallIntegerField(
                        blank=True, null=True, verbose_name="Number of footer rows"
                    ),
                ),
                (
                    "utc_date",
                    models.BooleanField(
                        default=False, verbose_name="Is time UTC? (substract 5 hours)"
                    ),
                ),
                ("date_column", models.SmallIntegerField(verbose_name="Date column")),
                ("time_column", models.SmallIntegerField(verbose_name="Time column")),
                (
                    "format_type",
                    models.CharField(
                        choices=[
                            ("automatic", "automatic"),
                            ("conventional", "conventional"),
                        ],
                        max_length=25,
                        verbose_name="Format type",
                    ),
                ),
                ("status", models.BooleanField(default=True, verbose_name="Status")),
                (
                    "date",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="formatting.date",
                        verbose_name="Date format",
                    ),
                ),
                (
                    "delimiter",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="formatting.delimiter",
                        verbose_name="Delimiter",
                    ),
                ),
                (
                    "extension",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="formatting.extension",
                        verbose_name="File extension",
                    ),
                ),
                (
                    "time",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="formatting.time",
                        verbose_name="Time format",
                    ),
                ),
            ],
            options={
                "ordering": ("-format_id",),
            },
        ),
        migrations.CreateModel(
            name="Classification",
            fields=[
                (
                    "cls_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="Id"
                    ),
                ),
                ("value", models.SmallIntegerField(verbose_name="Value column")),
                (
                    "maximum",
                    models.SmallIntegerField(
                        blank=True, null=True, verbose_name="Maximum value column"
                    ),
                ),
                (
                    "minimum",
                    models.SmallIntegerField(
                        blank=True, null=True, verbose_name="Minimum value column"
                    ),
                ),
                (
                    "value_validator_column",
                    models.SmallIntegerField(
                        blank=True, null=True, verbose_name="Value validator column"
                    ),
                ),
                (
                    "value_validator_text",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        null=True,
                        verbose_name="Value validator text",
                    ),
                ),
                (
                    "maximum_validator_column",
                    models.SmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Maximum value validator column",
                    ),
                ),
                (
                    "maximum_validator_text",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        null=True,
                        verbose_name="Maximum value  validator text",
                    ),
                ),
                (
                    "minimum_validator_column",
                    models.SmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Minimum value validator column",
                    ),
                ),
                (
                    "minimum_validator_text",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        null=True,
                        verbose_name="Minimum value validator text",
                    ),
                ),
                (
                    "accumulate",
                    models.BooleanField(
                        default=False, verbose_name="Accumulate every 5 min?"
                    ),
                ),
                (
                    "incremental",
                    models.BooleanField(
                        default=False, verbose_name="Is it an incremental counter?"
                    ),
                ),
                (
                    "resolution",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=6,
                        null=True,
                        verbose_name="Resolution",
                    ),
                ),
                (
                    "decimal_comma",
                    models.BooleanField(
                        default=False, verbose_name="Uses comma as decimal separator?"
                    ),
                ),
                (
                    "format",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="formatting.format",
                        verbose_name="Format",
                    ),
                ),
                (
                    "variable",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="variable.variable",
                        verbose_name="Variable",
                    ),
                ),
            ],
            options={
                "ordering": ("variable",),
            },
        ),
        migrations.CreateModel(
            name="Association",
            fields=[
                (
                    "association_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="Id"
                    ),
                ),
                (
                    "format",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="formatting.format",
                        verbose_name="Format",
                    ),
                ),
                (
                    "station",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="station.station",
                        verbose_name="Station",
                    ),
                ),
            ],
            options={
                "ordering": ("association_id",),
                "unique_together": {("station", "format")},
            },
        ),
    ]
