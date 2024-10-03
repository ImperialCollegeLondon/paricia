from management.views import (
    CustomCreateView,
    CustomDeleteView,
    CustomDetailView,
    CustomEditView,
)

from .models import Classification, Date, Delimiter, Extension, Format, Time


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
