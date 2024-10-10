"""Script to load initial data into the system such as stations, sensors, format types
etc. Currently data is stored in home/data but this will change in the future when
home is refactored.
"""

import json
import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import execute_from_command_line

from measurement.models import Measurement

# Get the superuser (the first one, if there are more than one)
User = get_user_model()
superuser = User.objects.filter(is_superuser=True).first()
if not superuser:
    raise ValueError("Superuser not found. Initial data cannot be loaded.")

# Create a temporary directory for the media files updated with the superuser
temp_dir = tempfile.TemporaryDirectory()

# The order matters so that foreignkey objects exist when an entry is created.
# The files are named app_model
data_files = [
    "variable_unit",
    "variable_variable",
    "formatting_delimiter",
    "formatting_extension",
    "formatting_date",
    "formatting_time",
    "formatting_format",
    "formatting_classification",
    "sensor_brand",
    "sensor_type",
    "station_type",
    "station_ecosystem",
    "station_country",
    "station_region",
    "station_place",
    "station_basin",
    "station_placebasin",
    "station_institution",
    "station_station",
    "measurement_airtemperature",
]

for file in data_files:
    # Measurement data is handled separately as it has no owner
    if "measurement" in file:
        shutil.copyfile(
            settings.BASE_DIR + "/utilities/data/" + file + ".json",
            temp_dir.name + "/" + file + ".json",
        )
        continue

    with open(settings.BASE_DIR + "/utilities/data/" + file + ".json") as f:
        data = json.load(f)

    for entry in data:
        entry["fields"]["owner"] = superuser.pk

    with open(temp_dir.name + "/" + file + ".json", "w") as f:
        json.dump(data, f)

# It's initially necessary to delete all measurements to avoid foreign key constraints
# And because this is "initial data", after all.
Measurement.objects.all().delete()

# Load all data files
for file in data_files:
    execute_from_command_line(
        [
            "manage.py",
            "loaddata",
            temp_dir.name + "/" + file + ".json",
        ]
    )

# Clean and save all measurements
for meas in Measurement.objects.all():
    meas.full_clean()
    meas.save()
