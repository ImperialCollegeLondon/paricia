import django_tables2 as tables

from .models import Classification, Date, Delimiter, Extension, Format, Time


class ExtensionTable(tables.Table):
    extension_id = tables.Column(linkify=True)

    class Meta:
        model = Extension
        fields = ["extension_id", "visibility", "value"]


class DelimiterTable(tables.Table):
    delimiter_id = tables.Column(linkify=True)

    class Meta:
        model = Delimiter
        fields = ["delimiter_id", "visibility", "name", "character"]


class DateTable(tables.Table):
    date_id = tables.Column(linkify=True)

    class Meta:
        model = Date
        fields = ["date_id", "visibility", "date_format", "code"]


class TimeTable(tables.Table):
    time_id = tables.Column(linkify=True)

    class Meta:
        model = Time
        fields = ["time_id"]


class FormatTable(tables.Table):
    format_id = tables.Column(linkify=True)
    extension = tables.Column(linkify=True)
    delimiter = tables.Column(linkify=True)
    date = tables.Column(linkify=True)
    time = tables.Column(linkify=True)

    class Meta:
        model = Format
        fields = [
            "format_id",
            "visibility",
            "name",
            "extension",
            "delimiter",
            "date",
            "time",
        ]


class ClassificationTable(tables.Table):
    cls_id = tables.Column(linkify=True)
    format = tables.Column(linkify=True)

    class Meta:
        model = Classification
        fields = ["cls_id", "visibility", "format", "variable"]
