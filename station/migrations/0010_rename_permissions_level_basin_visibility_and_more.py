# Generated by Django 5.0.3 on 2024-04-05 09:22

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("station", "0009_alter_basin_owner_alter_country_owner_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="basin",
            old_name="permissions_level",
            new_name="visibility",
        ),
        migrations.RenameField(
            model_name="country",
            old_name="permissions_level",
            new_name="visibility",
        ),
        migrations.RenameField(
            model_name="deltat",
            old_name="permissions_level",
            new_name="visibility",
        ),
        migrations.RenameField(
            model_name="ecosystem",
            old_name="permissions_level",
            new_name="visibility",
        ),
        migrations.RenameField(
            model_name="institution",
            old_name="permissions_level",
            new_name="visibility",
        ),
        migrations.RenameField(
            model_name="place",
            old_name="permissions_level",
            new_name="visibility",
        ),
        migrations.RenameField(
            model_name="placebasin",
            old_name="permissions_level",
            new_name="visibility",
        ),
        migrations.RenameField(
            model_name="region",
            old_name="permissions_level",
            new_name="visibility",
        ),
        migrations.RenameField(
            model_name="station",
            old_name="permissions_level",
            new_name="visibility",
        ),
        migrations.RenameField(
            model_name="stationtype",
            old_name="permissions_level",
            new_name="visibility",
        ),
    ]