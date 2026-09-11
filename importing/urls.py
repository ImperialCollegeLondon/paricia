from django.urls import path

from .views import (
    DataImportCreateView,
    DataImportDeleteView,
    DataImportDetailView,
    DataImportEditView,
    DataImportListView,
    DataImportUploadAPIView,
    DataIngestionQueryView,
    MapLayerCreateView,
    MapLayerDeleteView,
    MapLayerDetailView,
    MapLayerEditView,
    MapLayerListView,
    ThingsboardDataRetrievalView,
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
    path(
        "thingsboard-data-retrieval/",
        ThingsboardDataRetrievalView.as_view(),
        name="thingsboard_data_retrieval",
    ),
    path(
        "map-layers/",
        MapLayerListView.as_view(),
        name="maplayerimport_list",
    ),
    path(
        "map-layers/create/",
        MapLayerCreateView.as_view(),
        name="maplayerimport_create",
    ),
    path(
        "map-layers/<int:pk>/",
        MapLayerDetailView.as_view(),
        name="maplayerimport_detail",
    ),
    path(
        "map-layers/edit/<int:pk>/",
        MapLayerEditView.as_view(),
        name="maplayerimport_edit",
    ),
    path(
        "map-layers/delete/<int:pk>/",
        MapLayerDeleteView.as_view(),
        name="maplayerimport_delete",
    ),
]
