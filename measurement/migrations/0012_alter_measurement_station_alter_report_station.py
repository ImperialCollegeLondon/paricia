# Generated by Django 5.0.3 on 2024-03-24 21:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("measurement", "0011_alter_measurement_options_alter_report_options_and_more"),
        ("station", "0009_alter_basin_owner_alter_country_owner_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="measurement",
            name="station",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="station.station",
                verbose_name="Station",
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="station",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="station.station",
                verbose_name="Station",
            ),
        ),
    ]