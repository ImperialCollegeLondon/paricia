from django.urls import path

from .views import DataImportDetailView, DataImportEditView, DataImportListView

app_name = "importing"
urlpatterns = [
    path("", DataImportListView.as_view(), name="dataimport_list"),
    path("<int:pk>/", DataImportDetailView.as_view(), name="dataimport_detail"),
    path("edit/<int:pk>", DataImportEditView.as_view(), name="dataimport_edit"),
]
