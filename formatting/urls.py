from django.urls import path

from .views import (
    ClassificationDetailView,
    DateDetailView,
    DelimiterDetailView,
    ExtensionDetailView,
    FormatDetailView,
    TimeDetailView,
)

app_name = "formatting"
urlpatterns = [
    path("extension/<int:pk>", ExtensionDetailView.as_view(), name="extension_detail"),
    path("delimiter/<int:pk>", DelimiterDetailView.as_view(), name="delimiter_detail"),
    path("date/<int:pk>", DateDetailView.as_view(), name="date_detail"),
    path("time/<int:pk>", TimeDetailView.as_view(), name="time_detail"),
    path("format/<int:pk>", FormatDetailView.as_view(), name="format_detail"),
    path(
        "classification/<int:pk>",
        ClassificationDetailView.as_view(),
        name="classification_detail",
    ),
]
