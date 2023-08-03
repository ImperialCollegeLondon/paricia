from django_filters import rest_framework as filters

from station.models import Station


class DailyFilter(filters.FilterSet):
    """
    Filter class for hourlys that are not Polar Wind, Discharge Curve, or Level Function
    and that have no depth information.
    """

    date = filters.DateFilter(field_name="date", lookup_expr="exact")
    min_date = filters.DateFilter(field_name="date", lookup_expr="gte")
    max_date = filters.DateFilter(field_name="date", lookup_expr="lte")
    value = filters.NumberFilter(field_name="value", lookup_expr="exact")
    min_value = filters.NumberFilter(field_name="value", lookup_expr="gte")
    max_value = filters.NumberFilter(field_name="value", lookup_expr="lte")
    station_id = filters.NumberFilter(field_name="station_id", lookup_expr="exact")
    used_for_daily = filters.BooleanFilter(
        fieldname="used_for_daily", lookup_expr="exact"
    )


class DailyFilterDepth(DailyFilter):
    """
    Filter class for hourlys that are not Polar Wind, Discharge Curve, or Level Function
    and that have depth information.
    """

    depth = filters.NumberFilter(field_name="depth", lookup_expr="exact")
    min_depth = filters.NumberFilter(field_name="depth", lookup_expr="gte")
    max_depth = filters.NumberFilter(field_name="depth", lookup_expr="lte")
