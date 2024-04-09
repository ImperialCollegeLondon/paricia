from decimal import Decimal
from typing import Dict, List, Tuple

from django.db.models import Max, Min
from django_filters import rest_framework as filters

from measurement.models import Measurement

# class PolarWindFilter(filters.FilterSet):
#     """
#     Filter class for the Polar Wind validateds.
#     """
#
#     time = filters.DateTimeFilter(field_name="time", lookup_expr="exact")
#     min_time = filters.DateTimeFilter(field_name="time", lookup_expr="gte")
#     max_time = filters.DateTimeFilter(field_name="time", lookup_expr="lte")
#     speed = filters.NumberFilter(field_name="speed", lookup_expr="exact")
#     min_speed = filters.NumberFilter(field_name="speed", lookup_expr="gte")
#     max_speed = filters.NumberFilter(field_name="speed", lookup_expr="lte")
#     direction = filters.NumberFilter(field_name="direction", lookup_expr="exact")
#     min_direction = filters.NumberFilter(field_name="direction", lookup_expr="gte")
#     max_direction = filters.NumberFilter(field_name="direction", lookup_expr="lte")


# class DischargeCurveFilter(filters.FilterSet):
#     """
#     Filter class for the Discharge Curve validateds.
#     """
#
#     time = filters.DateTimeFilter(field_name="time", lookup_expr="exact")
#     min_time = filters.DateTimeFilter(field_name="time", lookup_expr="gte")
#     max_time = filters.DateTimeFilter(field_name="time", lookup_expr="lte")
#     require_recalculate_flow = filters.BooleanFilter(
#         field_name="require_recalculate_flow"
#     )
#     station = filters.ModelChoiceFilter(
#         field_name="station", queryset=Station.objects.all()
#     )


# class LevelFunctionFilter(filters.FilterSet):
#     """
#     Filter class for the Level Function validateds.
#     """
#
#     time = filters.DateTimeFilter(field_name="time", lookup_expr="exact")
#     min_time = filters.DateTimeFilter(field_name="time", lookup_expr="gte")
#     max_time = filters.DateTimeFilter(field_name="time", lookup_expr="lte")
#     discharge_curve = filters.ModelChoiceFilter(
#         field_name="discharge_curve", queryset=DischargeCurve.objects.all()
#     )
#     level = filters.NumberFilter(field_name="level", lookup_expr="exact")
#     min_level = filters.NumberFilter(field_name="level", lookup_expr="gte")
#     max_level = filters.NumberFilter(field_name="level", lookup_expr="lte")
#     function = filters.CharFilter(field_name="function", lookup_expr="icontains")


class ValidatedFilter(filters.FilterSet):
    """
    Filter class for validateds that are not Polar Wind, Discharge Curve, or Level Function
    and that have no depth information.
    """

    time = filters.DateTimeFilter(field_name="time", lookup_expr="exact")
    min_time = filters.DateTimeFilter(field_name="time", lookup_expr="gte")
    max_time = filters.DateTimeFilter(field_name="time", lookup_expr="lte")
    value = filters.NumberFilter(field_name="value", lookup_expr="exact")
    min_value = filters.NumberFilter(field_name="value", lookup_expr="gte")
    max_value = filters.NumberFilter(field_name="value", lookup_expr="lte")
    station_id = filters.NumberFilter(field_name="station_id", lookup_expr="exact")
    # TODO Include used_for_hourly
    used_for_hourly = filters.BooleanFilter(
        fieldname="used_for_hourly", lookup_expr="exact"
    )


class ValidatedFilterDepth(ValidatedFilter):
    """
    Filter class for validateds that are not Polar Wind, Discharge Curve, or Level Function
    and that have depth information.
    """

    depth = filters.NumberFilter(field_name="depth", lookup_expr="exact")
    min_depth = filters.NumberFilter(field_name="depth", lookup_expr="gte")
    max_depth = filters.NumberFilter(field_name="depth", lookup_expr="lte")


def get_station_options(station_codes: List[str]) -> Tuple[List[Dict], str]:
    """Get valid station options and default value based on permissions and data
    availability.

    Args:
        station_codes (list[str]): List of station codes based on permissions

    Returns:
        tuple[list[dict], str]: Options for the station dropdown, default value
    """

    stations_with_measurements = Measurement.objects.values_list(
        "station__station_code", flat=True
    ).distinct()

    station_options = [
        {"label": station_code, "value": station_code}
        for station_code in station_codes
        if station_code in stations_with_measurements
    ]
    station_value = station_options[0]["value"] if station_options else None
    return station_options, station_value


def get_variable_options(station: str) -> Tuple[List[Dict], str]:
    """Get valid variable options and default value based on the chosen station.

    Args:
        station (str): Code for the chosen station

    Returns:
        tuple[list[dict], str]: Options for the variable dropdown, default value
    """
    variable_dicts = (
        Measurement.objects.filter(station__station_code=station)
        .values("variable__name", "variable__variable_code")
        .distinct()
    )

    variable_options = [
        {
            "label": variable["variable__name"],
            "value": variable["variable__variable_code"],
        }
        for variable in variable_dicts
    ]
    variable_value = variable_options[0]["value"] if variable_options else None
    return variable_options, variable_value


def get_date_range(station: str, variable: str) -> Tuple[str, str]:
    """Get the date range covered by a chosen station and variable.

    Args:
        station (str): Code for the chosen station
        variable (str): Code for the chosen variable

    Returns:
        tuple[str, str]: Start date, end date
    """
    filter_vals = Measurement.objects.filter(
        station__station_code=station,
        variable__variable_code=variable,
    ).aggregate(
        first_date=Min("time"),
        last_date=Max("time"),
    )

    first_date = (
        filter_vals["first_date"].strftime("%Y-%m-%d")
        if filter_vals["first_date"]
        else None
    )
    last_date = (
        filter_vals["last_date"].strftime("%Y-%m-%d")
        if filter_vals["last_date"]
        else None
    )

    return first_date, last_date


def get_min_max(
    station, variable
) -> tuple[Decimal, Decimal,]:
    """Get the min and max of the data for a chosen station and variable.

    Args:
        station (str): Code for the chosen station
        variable (str): Code for the chosen variable

    Returns:
        tuple[Decimal, Decimal]: Min value, max value
    """
    filter_vals = Measurement.objects.filter(
        station__station_code=station,
        variable__variable_code=variable,
    ).aggregate(
        min_value=Min("minimum"),
        max_value=Max("maximum"),
    )

    min_value = filter_vals["min_value"] if filter_vals["min_value"] else None
    max_value = filter_vals["max_value"] if filter_vals["max_value"] else None

    return min_value, max_value
