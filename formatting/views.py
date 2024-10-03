from management.views import (
    CustomCreateView,
    CustomDeleteView,
    CustomDetailView,
    CustomEditView,
    CustomTableView,
)

from .filters import ClassificationFilter, FormatFilter
from .models import Classification, Date, Delimiter, Extension, Format, Time
from .tables import (
    ClassificationTable,
    DateTable,
    DelimiterTable,
    ExtensionTable,
    FormatTable,
    TimeTable,
)


# Detail views for formatting app.
class ExtensionDetailView(CustomDetailView):
    """View to view a extension."""

    model = Extension


class DelimiterDetailView(CustomDetailView):
    """View to view a delimiter."""

    model = Delimiter


class DateDetailView(CustomDetailView):
    """View to view a date."""

    model = Date


class TimeDetailView(CustomDetailView):
    """View to view a time."""

    model = Time


class FormatDetailView(CustomDetailView):
    """View to view a format."""

    model = Format


class ClassificationDetailView(CustomDetailView):
    """View to view a classification."""

    model = Classification


# Create views for formatting app.
class ExtensionCreateView(CustomCreateView):
    """View to create a extension."""

    model = Extension
    fields = "__all__"
    exclude = ["owner"]


class DelimiterCreateView(CustomCreateView):
    """View to create a delimiter."""

    model = Delimiter
    fields = "__all__"
    exclude = ["owner"]


class DateCreateView(CustomCreateView):
    """View to create a date."""

    model = Date
    fields = "__all__"
    exclude = ["owner"]


class TimeCreateView(CustomCreateView):
    """View to create a time."""

    model = Time
    fields = "__all__"
    exclude = ["owner"]


class FormatCreateView(CustomCreateView):
    """View to create a format."""

    model = Format
    fields = "__all__"
    exclude = ["owner"]
    foreign_key_fields = ["extension", "delimiter", "date", "time"]


class ClassificationCreateView(CustomCreateView):
    """View to create a classification."""

    model = Classification
    fields = "__all__"
    exclude = ["owner"]
    foreign_key_fields = ["format", "variable"]


# Edit views for formatting app.
class ExtensionEditView(CustomEditView):
    """View to edit a extension."""

    model = Extension
    fields = "__all__"
    exclude = ["owner"]


class DelimiterEditView(CustomEditView):
    """View to edit a delimiter."""

    model = Delimiter
    fields = "__all__"
    exclude = ["owner"]


class DateEditView(CustomEditView):
    """View to edit a date."""

    model = Date
    fields = "__all__"
    exclude = ["owner"]


class TimeEditView(CustomEditView):
    """View to edit a time."""

    model = Time
    fields = "__all__"
    exclude = ["owner"]


class FormatEditView(CustomEditView):
    """View to edit a format."""

    model = Format
    fields = "__all__"
    exclude = ["owner"]
    foreign_key_fields = ["extension", "delimiter", "date", "time"]


class ClassificationEditView(CustomEditView):
    """View to edit a classification."""

    model = Classification
    fields = "__all__"
    exclude = ["owner"]
    foreign_key_fields = ["format", "variable"]


# Delete views for formatting app.
class ExtensionDeleteView(CustomDeleteView):
    """View to delete a extension."""

    model = Extension


class DelimiterDeleteView(CustomDeleteView):
    """View to delete a delimiter."""

    model = Delimiter


class DateDeleteView(CustomDeleteView):
    """View to delete a date."""

    model = Date


class TimeDeleteView(CustomDeleteView):
    """View to delete a time."""

    model = Time


class FormatDeleteView(CustomDeleteView):
    """View to delete a format."""

    model = Format


class ClassificationDeleteView(CustomDeleteView):
    """View to delete a classification."""

    model = Classification


# List views for formatting app.
class ExtensionListView(CustomTableView):
    """View to list all extensions."""

    model = Extension
    table_class = ExtensionTable


class DelimiterListView(CustomTableView):
    """View to list all delimiters."""

    model = Delimiter
    table_class = DelimiterTable


class DateListView(CustomTableView):
    """View to list all dates."""

    model = Date
    table_class = DateTable


class TimeListView(CustomTableView):
    """View to list all times."""

    model = Time
    table_class = TimeTable


class FormatListView(CustomTableView):
    """View to list all formats."""

    model = Format
    table_class = FormatTable
    filterset_class = FormatFilter


class ClassificationListView(CustomTableView):
    """View to list all classifications."""

    model = Classification
    table_class = ClassificationTable
    filterset_class = ClassificationFilter
