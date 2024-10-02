from django.urls import path

from .views import DataImportDetailView, DataImportListView

app_name = "importing"
urlpatterns = [
    path("", DataImportListView.as_view(), name="dataimport_list"),
    path("<int:pk>/", DataImportDetailView.as_view(), name="dataimport_detail"),
]
