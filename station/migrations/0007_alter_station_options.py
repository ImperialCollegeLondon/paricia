# Generated by Django 5.0.2 on 2024-03-06 14:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("station", "0006_alter_country_options_placebasin_owner_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="station",
            options={
                "ordering": ("station_id",),
                "permissions": (("view_measurements", "View measurements"),),
            },
        ),
    ]