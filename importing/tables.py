import django_tables2 as tables

from .models import DataImport


class DataImportTable(tables.Table):
    data_import_id = tables.Column(linkify=True)

    class Meta:
        model = DataImport
        fields = (
            "data_import_id",
            "station",
            "format",
            "origin",
            "status",
            "date",
            "start_date",
            "end_date",
            "records",
        )
