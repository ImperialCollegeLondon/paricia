from management.views import CustomDetailView, CustomTableView

from .models import DataImport
from .tables import DataImportTable


class DataImportDetailView(CustomDetailView):
    """View to view a data import."""

    model = DataImport
    show_list_btn = True


class DataImportListView(CustomTableView):
    model = DataImport
    table_class = DataImportTable
    show_refresh_btn = True
