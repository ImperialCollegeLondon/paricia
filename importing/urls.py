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
        "create-thingsboard-map/",
        ThingsboardImportMapCreateView.as_view(),
        name="thingsboardimportmap_create",
    ),
    path(
        "create-thingsboard-map/",
        ThingsboardImportMapCreateView.as_view(),
        name="create_thingsboard_map",
    ),
]
