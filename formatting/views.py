from django.urls import reverse
from django.utils.safestring import mark_safe

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


def linkify(pk: int, address: str, label: str) -> str:
    """Return a link to the address with the label.

    Args:
        pk (int): Primary key of the object.
        address (str): URL address to link to. It must be a named URL, eg
            'app_name:model_detail'.
        label (str): Label to display on the link.

    Returns:
        str: HTML link to the address.
    """
    url = reverse(address, kwargs={"pk": pk})
    return mark_safe(f"<a href='{url}' class='btn btn-link'>{label}</a>")


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

    def get_inline(self) -> dict | None:
        """Return the inline data for the format.

        If provided, this method should return a dictionary with the inline data to be
        shown in the detail view. The dictionary should have the following keys:

        - title: Title of the inline data.
        - header: List with the header of the table.
        - objects: List with the objects to be shown in the table. Each object should be
            a list with the same length as the header.

        Returns:
            dict | None: Inline data for the format.
        """
        objects = [
            [
                linkify(obj.pk, "formatting:classification_detail", obj.pk),
                obj.value,
                obj.variable.name,
                linkify(
                    obj.variable.pk,
                    "variable:variable_detail",
                    obj.variable.variable_code,
                ),
                linkify(
                    obj.variable.unit.pk, "variable:unit_detail", obj.variable.unit
                ),
            ]
            for obj in self.object.classification_set.all()
        ]
        return {
            "title": "Classifications",
            "header": ["Id", "Column", "Variable", "Code", "Unit"],
            "objects": objects,
        }

    def get_url(self, pk, address, label):
        url = reverse(address, kwargs={"pk": pk})
        return mark_safe(f"<a href='{url}' class='btn btn-link'>{label}</a>")


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
