from django_filters import FilterSet, filters

from formatting.models import Format
from management.filters import FilterVisible
from station.models import Station

from .models import DataImport


class DataImportFilter(FilterSet):
    station = filters.ModelChoiceFilter(queryset=FilterVisible(DataImport, Station))
    format = filters.ModelChoiceFilter(queryset=FilterVisible(DataImport, Format))

    class Meta:
        model = DataImport
        fields = ["station", "format", "status"]
