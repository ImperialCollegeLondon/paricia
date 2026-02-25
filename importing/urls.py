from django.urls import path

from .views import (
    DataImportCreateView,
    DataImportDeleteView,
    DataImportDetailView,
    DataImportEditView,
    DataImportListView,
    DataImportUploadAPIView,
    DataIngestionQueryView,
    ThingsboardImportMapCreateView,
    ThingsboardImportMapDetailView,
    ThingsboardImportMapEditView,
    ThingsBoardImportMapListView,
)

app_name = "importing"
urlpatterns = [
    path("", DataImportListView.as_view(), name="dataimport_list"),
    path("<int:pk>/", DataImportDetailView.as_view(), name="dataimport_detail"),
    path("edit/<int:pk>", DataImportEditView.as_view(), name="dataimport_edit"),
    path("create/", DataImportCreateView.as_view(), name="dataimport_create"),
    path("delete/<int:pk>", DataImportDeleteView.as_view(), name="dataimport_delete"),
    path("api/upload/", DataImportUploadAPIView.as_view(), name="api_upload"),
    path(
        "api/dataingestion/",
        DataIngestionQueryView.as_view(),
        name="api_data_ingestion",
    ),
    path(
        "thingsboard-import-maps/",
        ThingsBoardImportMapListView.as_view(),
        name="thingsboardimportmap_list",
    ),
    path(
        "thingsboard-import-maps/create/",
        ThingsboardImportMapCreateView.as_view(),
        name="thingsboardimportmap_create",
    ),
    path(
        "thingsboard-import-maps/<int:pk>/",
        ThingsboardImportMapDetailView.as_view(),
        name="thingsboardimportmap_detail",
    ),
    path(
        "thingsboard-import-maps/edit/<int:pk>/",
        ThingsboardImportMapEditView.as_view(),
        name="thingsboardimportmap_edit",
    ),
    path(
        "thingsboard-import-maps/delete/<int:pk>/",
        ThingsboardImportMapEditView.as_view(),
        name="thingsboardimportmap_delete",
    ),
]
