from management.views import CustomDetailView

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
