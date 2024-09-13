from decimal import Decimal

from django.db.models import Max, Min

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


def get_variable_options(station: str) -> tuple[list[dict], str]:
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

    min_value = filter_vals["min_value"] if filter_vals["min_value"] else None
    max_value = filter_vals["max_value"] if filter_vals["max_value"] else None

    return min_value, max_value
