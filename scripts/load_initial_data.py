"""
Script to load initial data into the system such as stations, sensors, format types 
etc. Currently data is stored in home/data but this will change in the future when
home is refactored.
"""


from django.conf import settings
from django.core.management import execute_from_command_line

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
    "formatting_association",
]

for file in data_files:
    execute_from_command_line(
        ["manage.py", "loaddata", settings.BASE_DIR + "/home/data/" + file + ".json"]
    )