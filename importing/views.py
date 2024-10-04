from management.views import (
    CustomCreateView,
    CustomDeleteView,
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
    """View to list all data imports."""

    model = DataImport
    table_class = DataImportTable
    filterset_class = DataImportFilter


class DataImportEditView(CustomEditView):
    """View to edit a data import."""

    model = DataImport
    fields = ["visibility", "station", "format", "rawfile", "reprocess", "observations"]
    foreign_key_fields = ["station", "format"]


class DataImportCreateView(CustomCreateView):
    """View to create a data import."""

    model = DataImport
    fields = ["visibility", "station", "format", "rawfile", "reprocess", "observations"]
    foreign_key_fields = ["station", "format"]


class DataImportDeleteView(CustomDeleteView):
    """View to delete a data import."""

    model = DataImport
