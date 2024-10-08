from django.urls import path

from .views import (
    SensorBrandCreateView,
    SensorBrandDeleteView,
    SensorBrandDetailView,
    SensorBrandEditView,
    SensorBrandListView,
    SensorCreateView,
    SensorDeleteView,
    SensorDetailView,
    SensorEditView,
    SensorListView,
    SensorTypeCreateView,
    SensorTypeDeleteView,
    SensorTypeDetailView,
    SensorTypeEditView,
    SensorTypeListView,
)

app_name = "sensor"
urlpatterns = [
    path("sensor/<int:pk>", SensorDetailView.as_view(), name="sensor_detail"),
    path(
        "sensortype/<int:pk>", SensorTypeDetailView.as_view(), name="sensortype_detail"
    ),
    path(
        "sensorbrand/<int:pk>",
        SensorBrandDetailView.as_view(),
        name="sensorbrand_detail",
    ),
    path("sensor/create/", SensorCreateView.as_view(), name="sensor_create"),
    path(
        "sensortype/create/", SensorTypeCreateView.as_view(), name="sensortype_create"
    ),
    path(
        "sensorbrand/create/",
        SensorBrandCreateView.as_view(),
        name="sensorbrand_create",
    ),
    path("sensor/edit/<int:pk>", SensorEditView.as_view(), name="sensor_edit"),
    path(
        "sensortype/edit/<int:pk>", SensorTypeEditView.as_view(), name="sensortype_edit"
    ),
    path(
        "sensorbrand/edit/<int:pk>",
        SensorBrandEditView.as_view(),
        name="sensorbrand_edit",
    ),
    path("sensor/delete/<int:pk>", SensorDeleteView.as_view(), name="sensor_delete"),
    path(
        "sensortype/delete/<int:pk>",
        SensorTypeDeleteView.as_view(),
        name="sensortype_delete",
    ),
    path(
        "sensorbrand/delete/<int:pk>",
        SensorBrandDeleteView.as_view(),
        name="sensorbrand_delete",
    ),
    path("sensor/", SensorListView.as_view(), name="sensor_list"),
    path("sensortype/", SensorTypeListView.as_view(), name="sensortype_list"),
    path("sensorbrand/", SensorBrandListView.as_view(), name="sensorbrand_list"),
]
