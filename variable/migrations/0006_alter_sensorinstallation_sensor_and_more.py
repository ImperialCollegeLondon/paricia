# Generated by Django 5.1 on 2024-09-04 06:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sensor", "0006_alter_sensor_sensor_brand_alter_sensor_sensor_type"),
        ("station", "0012_alter_placebasin_basin_alter_placebasin_place_and_more"),
        (
            "variable",
            "0005_rename_permissions_level_sensorinstallation_visibility_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="sensorinstallation",
            name="sensor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="sensor.sensor",
                verbose_name="Sensor",
            ),
        ),
        migrations.AlterField(
            model_name="sensorinstallation",
            name="station",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="station.station",
                verbose_name="Station",
            ),
        ),
        migrations.AlterField(
            model_name="sensorinstallation",
            name="variable",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="variable.variable",
                verbose_name="Variable",
            ),
        ),
        migrations.AlterField(
            model_name="variable",
            name="unit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="variable.unit",
                verbose_name="Unit",
            ),
        ),
    ]