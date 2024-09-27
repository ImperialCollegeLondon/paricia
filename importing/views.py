from management.views import (
    CustomCreateView,
    CustomDetailView,
    CustomEditView,
    CustomTableView,
)

from .filters import DataImportFilter
from .models import DataImport
from .tables import DataImportTable


class DataImportDetailView(CustomDetailView):
    """View to view a data import."""

    model = DataImport


class DataImportListView(CustomTableView):
    model = DataImport
    table_class = DataImportTable
    filterset_class = DataImportFilter


class DataImportEditView(CustomEditView):
    model = DataImport
    fields = ["visibility", "station", "format", "rawfile", "reprocess", "observations"]
    foreign_key_fields = ["station", "format"]


class DataImportCreateView(CustomCreateView):
    model = DataImport
    fields = ["visibility", "station", "format", "rawfile", "reprocess", "observations"]
    foreign_key_fields = ["station", "format"]
