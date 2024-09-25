from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django_tables2 import RequestConfig
from guardian.shortcuts import get_objects_for_user

from management.views import CustomDetailView

from .models import DataImport
from .tables import DataImportTable


@login_required
def data_import_list(request: HttpRequest) -> HttpResponse:
    """View to list the data imports.

    This view lists the data imports that the user has permission to view.

    Args:
        request (HttpRequest): Object representing the request.

    Returns:
        HttpResponse: Response object with the rendered template.
    """
    table = DataImportTable(
        get_objects_for_user(request.user, "importing.view_dataimport")
    )
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(
        request,
        "table.html",
        {
            "table": table,
            "title": "Data imports",
            "refresh": "importing:dataimport_list",
        },
    )


class DataImportDetailView(CustomDetailView):
    """View to view a data import."""

    model = DataImport
    use_list_url = True
