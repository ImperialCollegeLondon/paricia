from management.views import (
    CustomCreateView,
    CustomDeleteView,
    CustomDetailView,
    CustomEditView,
    CustomTableView,
)

from .filters import SensorInstallationFilter, VariableFilter
from .models import SensorInstallation, Unit, Variable
from .tables import SensorInstallationTable, UnitTable, VariableTable


# Detail views for variable app.
class UnitDetailView(CustomDetailView):
    """View to view a unit."""

    model = Unit


class VariableDetailView(CustomDetailView):
    """View to view a variable."""

    model = Variable


class SensorInstallationDetailView(CustomDetailView):
    """View to view a sensor installation."""

    model = SensorInstallation


# Create views for variable app.
class UnitCreateView(CustomCreateView):
    """View to create a unit."""

    model = Unit
    exclude = ["owner"]


class VariableCreateView(CustomCreateView):
    """View to create a variable."""

    model = Variable
    exclude = ["owner"]


class SensorInstallationCreateView(CustomCreateView):
    """View to create a sensor installation."""

    model = SensorInstallation
    exclude = ["owner"]


# Edit views for variable app.
class UnitEditView(CustomEditView):
    """View to edit a unit."""

    model = Unit
    exclude = ["owner"]


class VariableEditView(CustomEditView):
    """View to edit a variable."""

    model = Variable
    exclude = ["owner"]


class SensorInstallationEditView(CustomEditView):
    """View to edit a sensor installation."""

    model = SensorInstallation
    exclude = ["owner"]


# Delete views for variable app.
class UnitDeleteView(CustomDeleteView):
    """View to delete a unit."""

    model = Unit


class VariableDeleteView(CustomDeleteView):
    """View to delete a variable."""

    model = Variable


class SensorInstallationDeleteView(CustomDeleteView):
    """View to delete a sensor installation."""

    model = SensorInstallation


# Table views for variable app.
class UnitListView(CustomTableView):
    """View to display a table of units."""

    model = Unit
    table_class = UnitTable


class VariableListView(CustomTableView):
    """View to display a table of variables."""

    model = Variable
    table_class = VariableTable
    filterset_class = VariableFilter


class SensorInstallationListView(CustomTableView):
    """View to display a table of sensor installations."""

    model = SensorInstallation
    table_class = SensorInstallationTable
    filterset_class = SensorInstallationFilter
