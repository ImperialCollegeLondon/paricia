import django_tables2 as tables

from .models import (
    Basin,
    Country,
    Ecosystem,
    Institution,
    Place,
    PlaceBasin,
    Region,
    Station,
    StationType,
)


class CountryTable(tables.Table):
    id = tables.Column(linkify=True)

    class Meta:
        model = Country
        fields = ["id", "visibility", "name"]


class RegionTable(tables.Table):
    id = tables.Column(linkify=True)
    country = tables.Column(linkify=True)

    class Meta:
        model = Region
        fields = ["id", "visibility", "name", "country"]


class EcosystemTable(tables.Table):
    id = tables.Column(linkify=True)

    class Meta:
        model = Ecosystem
        fields = ["id", "visibility", "name"]


class InstitutionTable(tables.Table):
    id = tables.Column(linkify=True)

    class Meta:
        model = Institution
        fields = ["id", "visibility", "name"]


class StationTypeTable(tables.Table):
    id = tables.Column(linkify=True)

    class Meta:
        model = StationType
        fields = ["id", "visibility", "name"]


class PlaceTable(tables.Table):
    id = tables.Column(linkify=True)

    class Meta:
        model = Place
        fields = ["id", "visibility", "name"]


class BasinTable(tables.Table):
    id = tables.Column(linkify=True)

    class Meta:
        model = Basin
        fields = ["id", "visibility", "name"]


class PlaceBasinTable(tables.Table):
    id = tables.Column(linkify=True)
    place = tables.Column(linkify=True)
    basin = tables.Column(linkify=True)

    class Meta:
        model = PlaceBasin
        fields = ["id", "visibility", "place", "basin"]


class StationTable(tables.Table):
    station_id = tables.Column(linkify=True)
    country = tables.Column(linkify=True)
    region = tables.Column(linkify=True)
    ecosystem = tables.Column(linkify=True)
    institution = tables.Column(linkify=True)
    station_type = tables.Column(linkify=True)
    place_basin = tables.Column(linkify=True)

    class Meta:
        model = Station
        fields = [
            "station_id",
            "visibility",
            "station_code",
            "station_name",
            "station_type",
            "country",
            "region",
            "ecosystem",
            "institution",
            "place_basin",
            "station_state",
        ]
