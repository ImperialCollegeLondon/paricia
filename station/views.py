from management.views import (
    CustomCreateView,
    CustomDeleteView,
    CustomDetailView,
    CustomEditView,
    CustomTableView,
)

from .filters import PlaceBasinFilter, RegionFilter, StationFilter
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
from .tables import (
    BasinTable,
    CountryTable,
    EcosystemTable,
    InstitutionTable,
    PlaceBasinTable,
    PlaceTable,
    RegionTable,
    StationTable,
    StationTypeTable,
)


# Detail views for station app.
class CountryDetailView(CustomDetailView):
    """View to view a country."""

    model = Country


class RegionDetailView(CustomDetailView):
    """View to view a region."""

    model = Region


class EcosystemDetailView(CustomDetailView):
    """View to view an ecosystem."""

    model = Ecosystem


class InstitutionDetailView(CustomDetailView):
    """View to view an institution."""

    model = Institution


class PlaceDetailView(CustomDetailView):
    """View to view a place."""

    model = Place


class StationTypeDetailView(CustomDetailView):
    """View to view a station type."""

    model = StationType


class BasinDetailView(CustomDetailView):
    """View to view a basin."""

    model = Basin


class PlaceBasinDetailView(CustomDetailView):
    """View to view a place basin."""

    model = PlaceBasin


class StationDetailView(CustomDetailView):
    """View to view a station."""

    model = Station


# Create views for station app.
class CountryCreateView(CustomCreateView):
    """View to create a country."""

    model = Country
    exclude = ["owner"]


class RegionCreateView(CustomCreateView):
    """View to create a region."""

    model = Region
    exclude = ["owner"]


class EcosystemCreateView(CustomCreateView):
    """View to create an ecosystem."""

    model = Ecosystem
    exclude = ["owner"]


class InstitutionCreateView(CustomCreateView):
    """View to create an institution."""

    model = Institution
    exclude = ["owner"]


class PlaceCreateView(CustomCreateView):
    """View to create a place."""

    model = Place
    exclude = ["owner"]


class StationTypeCreateView(CustomCreateView):
    """View to create a station type."""

    model = StationType
    exclude = ["owner"]


class BasinCreateView(CustomCreateView):
    """View to create a basin."""

    model = Basin
    exclude = ["owner"]


class PlaceBasinCreateView(CustomCreateView):
    """View to create a place basin."""

    model = PlaceBasin
    exclude = ["owner"]


class StationCreateView(CustomCreateView):
    """View to create a station."""

    model = Station
    exclude = ["owner"]


# Edit views for station app.
class CountryEditView(CustomEditView):
    """View to edit a country."""

    model = Country
    exclude = ["owner"]


class RegionEditView(CustomEditView):
    """View to edit a region."""

    model = Region
    exclude = ["owner"]


class EcosystemEditView(CustomEditView):
    """View to edit an ecosystem."""

    model = Ecosystem
    exclude = ["owner"]


class InstitutionEditView(CustomEditView):
    """View to edit an institution."""

    model = Institution
    exclude = ["owner"]


class PlaceEditView(CustomEditView):
    """View to edit a place."""

    model = Place
    exclude = ["owner"]


class StationTypeEditView(CustomEditView):
    """View to edit a station type."""

    model = StationType
    exclude = ["owner"]


class BasinEditView(CustomEditView):
    """View to edit a basin."""

    model = Basin
    exclude = ["owner"]


class PlaceBasinEditView(CustomEditView):
    """View to edit a place basin."""

    model = PlaceBasin
    exclude = ["owner"]


class StationEditView(CustomEditView):
    """View to edit a station."""

    model = Station
    exclude = ["owner"]


# Delete views for station app.
class CountryDeleteView(CustomDeleteView):
    """View to delete a country."""

    model = Country


class RegionDeleteView(CustomDeleteView):
    """View to delete a region."""

    model = Region


class EcosystemDeleteView(CustomDeleteView):
    """View to delete an ecosystem."""

    model = Ecosystem


class InstitutionDeleteView(CustomDeleteView):
    """View to delete an institution."""

    model = Institution


class PlaceDeleteView(CustomDeleteView):
    """View to delete a place."""

    model = Place


class StationTypeDeleteView(CustomDeleteView):
    """View to delete a station type."""

    model = StationType


class BasinDeleteView(CustomDeleteView):
    """View to delete a basin."""

    model = Basin


class PlaceBasinDeleteView(CustomDeleteView):
    """View to delete a place basin."""

    model = PlaceBasin


class StationDeleteView(CustomDeleteView):
    """View to delete a station."""

    model = Station


# Table views for station app.
class CountryTableView(CustomTableView):
    """View to display a table of countries."""

    model = Country
    table_class = CountryTable


class RegionTableView(CustomTableView):
    """View to display a table of regions."""

    model = Region
    table_class = RegionTable
    filterset_class = RegionFilter


class EcosystemTableView(CustomTableView):
    """View to display a table of ecosystems."""

    model = Ecosystem
    table_class = EcosystemTable


class InstitutionTableView(CustomTableView):
    """View to display a table of institutions."""

    model = Institution
    table_class = InstitutionTable


class PlaceTableView(CustomTableView):
    """View to display a table of places."""

    model = Place
    table_class = PlaceTable


class StationTypeTableView(CustomTableView):
    """View to display a table of station types."""

    model = StationType
    table_class = StationTypeTable


class BasinTableView(CustomTableView):
    """View to display a table of basins."""

    model = Basin
    table_class = BasinTable


class PlaceBasinTableView(CustomTableView):
    """View to display a table of place basins."""

    model = PlaceBasin
    table_class = PlaceBasinTable
    filterset_class = PlaceBasinFilter


class StationTableView(CustomTableView):
    """View to display a table of stations."""

    model = Station
    table_class = StationTable
    filterset_class = StationFilter
