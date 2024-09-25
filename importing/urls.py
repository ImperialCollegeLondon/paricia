from django.urls import path

from .views import DataImportDetailView, data_import_list

app_name = "importing"
urlpatterns = [
    path("", data_import_list, name="dataimport_list"),
    path("<int:pk>/", DataImportDetailView.as_view(), name="dataimport_detail"),
]
