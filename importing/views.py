from contextlib import suppress

from django import forms
from django.contrib.auth.decorators import login_required
from django.db.models import ForeignKey, Model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django_tables2 import RequestConfig
from guardian.shortcuts import get_objects_for_user

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
        {"table": table, "title": "Data imports", "refresh": "import:data_import_list"},
    )


def model_to_dict(instance: Model) -> dict:
    """Convert a model instance to a dictionary.

    For ForeignKey fields, the related model instance is converted to a string, so that
    a meaningful representation is shown in the dictionary instead of the primary key.

    Args:
        instance (Model): Model instance to convert.

    Returns:
        dict: Dictionary with the model instance data.
    """
    data = {}
    for field in instance._meta.get_fields():
        data[field.name] = field.value_from_object(instance)
        if isinstance(field, ForeignKey):
            with suppress(field.related_model.DoesNotExist):
                data[field.name] = str(
                    field.related_model.objects.get(pk=data[field.name])
                )
    return data


@login_required
def data_import_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to view a data import.

    This view shows the details of a data import. The user must have permission to view
    the data import object, otherwise a 403 error is returned.

    Args:
        request (HttpRequest): Object representing the request.
        pk (int): Primary key of the data import object.

    Returns:
        HttpResponse: Response object with the rendered template.
    """

    class DataImportForm(forms.ModelForm):
        class Meta:
            model = DataImport
            fields = "__all__"

    instance = get_object_or_404(DataImport, pk=pk)
    if not request.user.has_perm("importing.view_dataimport", instance):
        return render(request, "403.html", status=403)

    form = DataImportForm(data=model_to_dict(instance))
    return render(
        request,
        "object_detail.html",
        {"form": form, "back_url": "import:data_import_list"},
    )
