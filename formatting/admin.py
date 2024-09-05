from django.contrib import admin

from management.admin import PermissionsBaseAdmin

from .models import (
    Classification,
    Date,
    Delimiter,
    Extension,
    Format,
    Time,
)

admin.site.site_header = "Paricia Administration - Formatting"


@admin.register(Extension)
class ExtensionAdmin(PermissionsBaseAdmin):
    """Admin class for the Extension model."""

    list_display = ["extension_id", "value"]


@admin.register(Delimiter)
class DelimiterAdmin(PermissionsBaseAdmin):
    """Admin class for the Delimiter model."""

    list_display = ["delimiter_id", "name", "character"]


@admin.register(Date)
class DateAdmin(PermissionsBaseAdmin):
    """Admin class for the Date model."""

    list_display = ["date_id", "date_format", "code"]


@admin.register(Time)
class TimeAdmin(PermissionsBaseAdmin):
    """Admin class for the Time model."""

    list_display = ["time_id", "time_format", "code"]


@admin.register(Format)
class FormatAdmin(PermissionsBaseAdmin):
    """Admin class for the Format model."""

    list_display = [
        "format_id",
        "name",
        "extension",
        "delimiter",
        "date",
        "date_column",
        "time",
        "time_column",
        "first_row",
        "footer_rows",
    ]


@admin.register(Classification)
class ClassificationAdmin(PermissionsBaseAdmin):
    """Admin class for the Classification model."""

    list_display = [
        "cls_id",
        "format",
        "variable",
        "value",
        "accumulate",
        "incremental",
        "resolution",
    ]
