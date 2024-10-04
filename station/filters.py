from django_filters import FilterSet, filters

from management.filters import FilterVisible

from .models import (
    Basin,
    Country,
    Institution,
    Place,
    PlaceBasin,
    Region,
    Station,
    StationType,
)


class RegionFilter(FilterSet):
    country = filters.ModelChoiceFilter(queryset=FilterVisible(Region, Country))

    class Meta:
        model = Region
        fields = ["visibility", "country"]


class PlaceBasinFilter(FilterSet):
    place = filters.ModelChoiceFilter(queryset=FilterVisible(PlaceBasin, Place))
    basin = filters.ModelChoiceFilter(queryset=FilterVisible(PlaceBasin, Basin))

    class Meta:
        model = PlaceBasin
        fields = ["visibility", "place", "basin"]


class StationFilter(FilterSet):
    station_type = filters.ModelChoiceFilter(Station, StationType, "station_type")
    region = filters.ModelChoiceFilter(queryset=FilterVisible(Station, Region))
    country = filters.ModelChoiceFilter(queryset=FilterVisible(Station, Country))
    institution = filters.ModelChoiceFilter(
        queryset=FilterVisible(Station, Institution)
    )
    place_basin = filters.ModelChoiceFilter(
        queryset=FilterVisible(Station, PlaceBasin, "place_basin")
    )

    class Meta:
        model = Station
        fields = [
            "visibility",
            "station_type",
            "region",
            "country",
            "institution",
            "place_basin",
        ]
