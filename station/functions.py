from measurement.models import Measurement

from .models import Station


def update_variables_for_station(*station_codes) -> None:
    """Update the variables for the given station codes.

    The variables are updated based on the measurements associated with the station.
    The variables are saved as a comma-separated string in the variables field of the
    station model.

    Args:
        station_codes (tuple[str]): Station codes for which to update the variables.
            If not provided, all station codes with measurements are considered.
    """

    # We get the station codes from the Measurement model if not provided
    # Only station codes with measurements are considered
    station_codes = (
        station_codes
        or Measurement.objects.values_list(
            "station__station_code", flat=True
        ).distinct()
    )

    # Get the variables for each station and save them as a comma-separated string
    for station_code in station_codes:
        variables = (
            Measurement.objects.filter(station__station_code=station_code)
            .values_list("variable__variable_code", flat=True)
            .distinct()
        )
        if variables:
            station = Station.objects.get(station_code=station_code)
            station.variables = variables = ",".join(variables)
            station.full_clean()
            station.save()
