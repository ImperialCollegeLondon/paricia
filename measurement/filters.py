from django_filters import rest_framework as filters


class MeasurementFilter(filters.FilterSet):
    time = filters.DateTimeFilter(field_name="time", lookup_expr="exact")
    min_time = filters.DateTimeFilter(field_name="time", lookup_expr="gte")
    max_time = filters.DateTimeFilter(field_name="time", lookup_expr="lte")
    value = filters.NumberFilter(field_name="value", lookup_expr="exact")
    min_value = filters.NumberFilter(field_name="value", lookup_expr="gte")
    max_value = filters.NumberFilter(field_name="value", lookup_expr="lte")
    station_id = filters.NumberFilter(field_name="station_id", lookup_expr="exact")


class MeasurementFilterDepth(MeasurementFilter):
    depth = filters.NumberFilter(field_name="depth", lookup_expr="exact")
    min_depth = filters.NumberFilter(field_name="depth", lookup_expr="gte")
    max_depth = filters.NumberFilter(field_name="depth", lookup_expr="lte")
