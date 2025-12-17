from django.urls import path

from .views import (
    DataImportCreateView,
    DataImportDeleteView,
    DataImportDetailView,
    DataImportEditView,
    DataImportListView,
    DataImportUploadAPIView,
    DataingestionQueryView,
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
        "api/dataingestion/", DataingestionQueryView.as_view(), name="api_dataingestion"
    ),
]
