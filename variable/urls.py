from django.urls import path

from .views import (
    SensorInstallationCreateView,
    SensorInstallationDeleteView,
    SensorInstallationDetailView,
    SensorInstallationEditView,
    SensorInstallationListView,
    UnitCreateView,
    UnitDeleteView,
    UnitDetailView,
    UnitEditView,
    UnitListView,
    VariableCreateView,
    VariableDeleteView,
    VariableDetailView,
    VariableEditView,
    VariableListView,
)

app_name = "variable"
urlpatterns = [
    path("unit/<int:pk>", UnitDetailView.as_view(), name="unit_detail"),
    path("variable/<int:pk>", VariableDetailView.as_view(), name="variable_detail"),
    path(
        "sensorinstallation/<int:pk>",
        SensorInstallationDetailView.as_view(),
        name="sensorinstallation_detail",
    ),
    path("unit/create/", UnitCreateView.as_view(), name="unit_create"),
    path("variable/create/", VariableCreateView.as_view(), name="variable_create"),
    path(
        "sensorinstallation/create/",
        SensorInstallationCreateView.as_view(),
        name="sensorinstallation_create",
    ),
    path("unit/edit/<int:pk>", UnitEditView.as_view(), name="unit_edit"),
    path("variable/edit/<int:pk>", VariableEditView.as_view(), name="variable_edit"),
    path(
        "sensorinstallation/edit/<int:pk>",
        SensorInstallationEditView.as_view(),
        name="sensorinstallation_edit",
    ),
    path("unit/delete/<int:pk>", UnitDeleteView.as_view(), name="unit_delete"),
    path(
        "variable/delete/<int:pk>", VariableDeleteView.as_view(), name="variable_delete"
    ),
    path(
        "sensorinstallation/delete/<int:pk>",
        SensorInstallationDeleteView.as_view(),
        name="sensorinstallation_delete",
    ),
    path("unit/", UnitListView.as_view(), name="unit_list"),
    path("variable/", VariableListView.as_view(), name="variable_list"),
    path(
        "sensorinstallation/",
        SensorInstallationListView.as_view(),
        name="sensorinstallation_list",
    ),
]
