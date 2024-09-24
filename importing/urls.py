from django.urls import path

from .views import data_import_list, data_import_view

app_name = "import"
urlpatterns = [
    path("", data_import_list, name="data_import_list"),
    path("<int:pk>/", data_import_view, name="data_import_detail"),
]
