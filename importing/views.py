from contextlib import suppress

from django import forms
from django.contrib.auth.decorators import login_required
from django.db.models import ForeignKey, Model
from django.shortcuts import get_object_or_404, render
from django_tables2 import RequestConfig

from .models import DataImport
from .tables import DataImportTable


@login_required
def data_import_list(request):
    table = DataImportTable(DataImport.objects.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(
        request,
        "table.html",
        {"table": table, "title": "Data imports", "refresh": "import:data_import_list"},
    )


def model_to_dict(instance: Model) -> dict:
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
def data_import_view(request, pk):
    class DataImportForm(forms.ModelForm):
        class Meta:
            model = DataImport
            fields = "__all__"

    model = get_object_or_404(DataImport, pk=pk)
    form = DataImportForm(data=model_to_dict(model), instance=model)
    return render(
        request,
        "object_detail.html",
        {"form": form, "back_url": "import:data_import_list"},
    )
