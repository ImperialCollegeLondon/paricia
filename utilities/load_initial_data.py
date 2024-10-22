"""Script to load initial data into the system such as stations, sensors, format types
etc. Currently data is stored in home/data but this will change in the future when
home is refactored.
"""

from django.conf import settings
from django.core.management import execute_from_command_line

from measurement.models import Measurement
from station.functions import update_variables_for_station

# The order matters so that foreignkey objects exist when an entry is created.
# The files are named app_model
data_files = [
    "management_user",
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

# It's initially necessary to delete all measurements to avoid foreign key constraints
# And because this is "initial data", after all.
Measurement.objects.all().delete()

# Load all data files
for file in data_files:
    execute_from_command_line(
        [
            "manage.py",
            "loaddata",
            settings.BASE_DIR + "/utilities/data/" + file + ".json",
        ]
    )

# Clean and save all measurements
for meas in Measurement.objects.all():
    meas.full_clean()
    meas.save()

update_variables_for_station()
