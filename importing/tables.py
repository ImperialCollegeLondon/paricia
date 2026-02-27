import django_tables2 as tables

from .models import DataImport, ThingsboardImportMap


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


class ThingsboardImportMapTable(tables.Table):
    pk = tables.Column(linkify=True)

    class Meta:
        model = ThingsboardImportMap
        fields = (
            "pk",
            "tb_variable",
            "variable",
            "device_id",
            "station",
        )
