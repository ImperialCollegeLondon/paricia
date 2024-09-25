from django.db.models.query import QuerySet
from django.http import HttpRequest
from django_filters import FilterSet, filters
from guardian.shortcuts import get_objects_for_user

from .models import DataImport


def stations(request: HttpRequest) -> QuerySet:
    """Return the stations the user has permission to view.

    If request is None, return an empty queryset.

    Args:
        request (HttpRequest): Request object.

    Returns:
        QuerySet: Stations the user has permission to view
    """
    if request is None:
        return DataImport.objects.none()

    user = request.user
    return (
        get_objects_for_user(user, "importing.view_dataimport", klass=DataImport)
        .values_list("station__station_code", flat=True)
        .distinct()
    )


class DataImportFilter(FilterSet):
    station = filters.ModelChoiceFilter(queryset=stations)

    class Meta:
        model = DataImport
        fields = ["station", "status"]
