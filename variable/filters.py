from django_filters import FilterSet, filters

from management.filters import FilterVisible
from sensor.models import Sensor
from station.models import Station

from .models import SensorInstallation, Unit, Variable


class VariableFilter(FilterSet):
    unit = filters.ModelChoiceFilter(queryset=FilterVisible(Variable, Unit))

    class Meta:
        model = Variable
        fields = ["visibility", "unit"]


class SensorInstallationFilter(FilterSet):
    variable = filters.ModelChoiceFilter(
        queryset=FilterVisible(SensorInstallation, Variable)
    )
    station = filters.ModelChoiceFilter(
        queryset=FilterVisible(SensorInstallation, Station)
    )
    sensor = filters.ModelChoiceFilter(
        queryset=FilterVisible(SensorInstallation, Sensor)
    )

    class Meta:
        model = SensorInstallation
        fields = ["visibility", "variable", "station", "sensor"]
