import django_tables2 as tables

from .models import SensorInstallation, Unit, Variable


class UnitTable(tables.Table):
    unit_id = tables.Column(linkify=True)

    class Meta:
        model = Unit
        fields = ["unit_id", "visibility", "name", "initials"]


class VariableTable(tables.Table):
    variable_id = tables.Column(linkify=True)
    unit = tables.Column(linkify=True)

    class Meta:
        model = Variable
        fields = ["variable_id", "visibility", "variable_code", "name", "unit"]


class SensorInstallationTable(tables.Table):
    sensorinstallation_id = tables.Column(linkify=True)
    variable = tables.Column(linkify=True)
    # station = tables.Column(linkify=True)
    # sensor = tables.Column(linkify=True)

    class Meta:
        model = SensorInstallation
        fields = [
            "sensorinstallation_id",
            "visibility",
            "variable",
            "station",
            "sensor",
            "state",
        ]
