from django.urls import path

from .views import data_import_detail_view, data_import_list

app_name = "import"
urlpatterns = [
    path("", data_import_list, name="data_import_list"),
    path("<int:pk>/", data_import_detail_view, name="data_import_detail"),
]
