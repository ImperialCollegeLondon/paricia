from management.views import (
    CustomCreateView,
    CustomDeleteView,
    CustomDetailView,
    CustomEditView,
    CustomTableView,
)

from .filters import SensorFilter
from .models import Sensor, SensorBrand, SensorType
from .tables import SensorBrandTable, SensorTable, SensorTypeTable


# Detail views for sensor app.
class SensorDetailView(CustomDetailView):
    """View to view a sensor."""

    model = Sensor


class SensorTypeDetailView(CustomDetailView):
    """View to view a sensor type."""

    model = SensorType


class SensorBrandDetailView(CustomDetailView):
    """View to view a sensor brand."""

    model = SensorBrand


# Create views for sensor app.
class SensorCreateView(CustomCreateView):
    """View to create a sensor."""

    model = Sensor
    exclude = ["owner"]


class SensorTypeCreateView(CustomCreateView):
    """View to create a sensor type."""

    model = SensorType
    exclude = ["owner"]


class SensorBrandCreateView(CustomCreateView):
    """View to create a sensor brand."""

    model = SensorBrand
    exclude = ["owner"]


# Edit views for sensor app.
class SensorEditView(CustomEditView):
    """View to edit a sensor."""

    model = Sensor
    exclude = ["owner"]


class SensorTypeEditView(CustomEditView):
    """View to edit a sensor type."""

    model = SensorType
    exclude = ["owner"]


class SensorBrandEditView(CustomEditView):
    """View to edit a sensor brand."""

    model = SensorBrand
    exclude = ["owner"]


# Delete views for sensor app.
class SensorDeleteView(CustomDeleteView):
    """View to delete a sensor."""

    model = Sensor


class SensorTypeDeleteView(CustomDeleteView):
    """View to delete a sensor type."""

    model = SensorType


class SensorBrandDeleteView(CustomDeleteView):
    """View to delete a sensor brand."""

    model = SensorBrand


# Table views for sensor app.
class SensorListView(CustomTableView):
    """View to list sensors."""

    model = Sensor
    table_class = SensorTable
    filterset_class = SensorFilter


class SensorTypeListView(CustomTableView):
    """View to list sensor types."""

    model = SensorType
    table_class = SensorTypeTable


class SensorBrandListView(CustomTableView):
    """View to list sensor brands."""

    model = SensorBrand
    table_class = SensorBrandTable
