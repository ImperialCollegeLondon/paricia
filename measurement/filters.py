from django_filters import rest_framework as filters

from measurement.models import DischargeCurve
from station.models import Station


class PolarWindFilter(filters.FilterSet):
    """
    Filter class for the Polar Wind measurements.
    """

    time = filters.DateTimeFilter(field_name="time", lookup_expr="exact")
    min_time = filters.DateTimeFilter(field_name="time", lookup_expr="gte")
    max_time = filters.DateTimeFilter(field_name="time", lookup_expr="lte")
    speed = filters.NumberFilter(field_name="speed", lookup_expr="exact")
    min_speed = filters.NumberFilter(field_name="speed", lookup_expr="gte")
    max_speed = filters.NumberFilter(field_name="speed", lookup_expr="lte")
    direction = filters.NumberFilter(field_name="direction", lookup_expr="exact")
    min_direction = filters.NumberFilter(field_name="direction", lookup_expr="gte")
    max_direction = filters.NumberFilter(field_name="direction", lookup_expr="lte")


class DischargeCurveFilter(filters.FilterSet):
    """
    Filter class for the Discharge Curve measurements.
    """

    time = filters.DateTimeFilter(field_name="time", lookup_expr="exact")
    min_time = filters.DateTimeFilter(field_name="time", lookup_expr="gte")
    max_time = filters.DateTimeFilter(field_name="time", lookup_expr="lte")
    require_recalculate_flow = filters.BooleanFilter(
        field_name="require_recalculate_flow"
    )
    station = filters.ModelChoiceFilter(
        field_name="station", queryset=Station.objects.all()
    )


class LevelFunctionFilter(filters.FilterSet):
    """
    Filter class for the Level Function measurements.
    """

    time = filters.DateTimeFilter(field_name="time", lookup_expr="exact")
    min_time = filters.DateTimeFilter(field_name="time", lookup_expr="gte")
    max_time = filters.DateTimeFilter(field_name="time", lookup_expr="lte")
    discharge_curve = filters.ModelChoiceFilter(
        field_name="discharge_curve", queryset=DischargeCurve.objects.all()
    )
    level = filters.NumberFilter(field_name="level", lookup_expr="exact")
    min_level = filters.NumberFilter(field_name="level", lookup_expr="gte")
    max_level = filters.NumberFilter(field_name="level", lookup_expr="lte")
    function = filters.CharFilter(field_name="function", lookup_expr="icontains")


class MeasurementFilter(filters.FilterSet):
    """
    Filter class for measurements that are not Polar Wind, Discharge Curve, or Level Function
    and that have no depth information.
    """

    time = filters.DateTimeFilter(field_name="time", lookup_expr="exact")
    min_time = filters.DateTimeFilter(field_name="time", lookup_expr="gte")
    max_time = filters.DateTimeFilter(field_name="time", lookup_expr="lte")
    value = filters.NumberFilter(field_name="value", lookup_expr="exact")
    min_value = filters.NumberFilter(field_name="value", lookup_expr="gte")
    max_value = filters.NumberFilter(field_name="value", lookup_expr="lte")
    station_id = filters.NumberFilter(field_name="station_id", lookup_expr="exact")


class MeasurementFilterDepth(MeasurementFilter):
    """
    Filter class for measurements that are not Polar Wind, Discharge Curve, or Level Function
    and that have depth information.
    """

    depth = filters.NumberFilter(field_name="depth", lookup_expr="exact")
    min_depth = filters.NumberFilter(field_name="depth", lookup_expr="gte")
    max_depth = filters.NumberFilter(field_name="depth", lookup_expr="lte")
