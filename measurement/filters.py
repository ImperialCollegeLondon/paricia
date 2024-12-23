from decimal import Decimal

from django.db.models import Max, Min, Q

from station.models import Station
from utilities.timezones import to_local_time
from variable.models import Variable

from .models import Measurement


def get_station_options(
    station_codes: list[str],
) -> tuple[list[dict[str, str]], str | None]:
    """Get valid station options and default value based on permissions and data
    availability.

    Args:
        station_codes (list[str]): List of station codes based on permissions

    Returns:
        tuple[list[dict], str]: Options for the station dropdown, default value
    """
    stations_with_measurements = Station.objects.filter(
        ~Q(variables=""), station_code__in=station_codes
    ).values_list("station_code", flat=True)

    station_options = [
        {"label": station_code, "value": station_code}
        for station_code in stations_with_measurements
    ]
    station_value = station_options[0]["value"] if station_options else None
    return station_options, station_value


def get_variable_options(station: str) -> tuple[list[dict[str, str]], str | None]:
    """Get valid variable options and default value based on the chosen station.

    Args:
        station (str): Code for the chosen station

    Returns:
        tuple[list[dict], str]: Options for the variable dropdown, default value
    """
    variable_codes = Station.objects.get(station_code=station).variables_list
    variable_dicts = Variable.objects.filter(variable_code__in=variable_codes).values(
        "name", "variable_code"
    )

    variable_options = [
        {
            "label": variable["name"],
            "value": variable["variable_code"],
        }
        for variable in variable_dicts
    ]

    variable_value = variable_options[0]["value"] if variable_options else None
    return variable_options, variable_value


def get_date_range(station: str, variable: str) -> tuple[str, str]:
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

    first_date = to_local_time(filter_vals["first_date"]).strftime("%Y-%m-%d")
    last_date = to_local_time(filter_vals["last_date"]).strftime("%Y-%m-%d")
    return first_date, last_date


def get_min_max(
    station, variable
) -> tuple[
    Decimal,
    Decimal,
]:
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

    min_value = filter_vals["min_value"]
    max_value = filter_vals["max_value"]

    return min_value, max_value
