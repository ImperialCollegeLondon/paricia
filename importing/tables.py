import django_tables2 as tables

from .models import DataImport, MapLayerImport, ThingsboardImportMap


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
            "tb_device_name",
            "station",
        )


class MapLayerImportTable(tables.Table):
    pk = tables.Column(linkify=True)

    class Meta:
        model = MapLayerImport
        fields = (
            "pk",
            "name",
            "description",
        )
