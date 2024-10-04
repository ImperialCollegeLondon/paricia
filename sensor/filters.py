from django_filters import FilterSet, filters

from management.filters import FilterVisible

from .models import Sensor, SensorBrand, SensorType


class SensorFilter(FilterSet):
    sensor_type = filters.ModelChoiceFilter(
        queryset=FilterVisible(Sensor, SensorType, "sensor_type")
    )
    sensor_brand = filters.ModelChoiceFilter(
        queryset=FilterVisible(Sensor, SensorBrand, "sensor_brand")
    )

    class Meta:
        model = Sensor
        fields = ["visibility", "sensor_type", "sensor_brand"]
