########################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos
# (iMHEA)basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#           Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS),
#           Ecuador.
#           Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones
#  creadoras, ya sea en uso total o parcial del código.
########################################################################################

from __future__ import unicode_literals

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from utilities.functions import modelo_a_tabla_html

from .forms import ClassificationForm
from .models import (
    Association,
    Classification,
    Date,
    Delimiter,
    Extension,
    Format,
    Time,
)


#################################################################
# Date
class DateCreate(PermissionRequiredMixin, CreateView):
    permission_required = "format.add_fecha"
    model = Date
    fields = ["format", "code"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context


class DateList(PermissionRequiredMixin, TemplateView):
    permission_required = "format.view_fecha"
    template_name = "format/fecha_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = ["date_id", "format", "code"]
        model = Date.objects.values_list(*fields)
        context["dates"] = modelo_a_tabla_html(model, col_extra=True)
        return context


class DateDetail(PermissionRequiredMixin, DetailView):
    model = Date
    permission_required = "format.view_fecha"


class DateUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "format.change_date"
    model = Date
    fields = ["format", "code"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modify"
        return context


class DateDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "format.delete_date"
    model = Date
    success_url = reverse_lazy("format:date_index")


#################################################################
# Time
class TimeCreate(PermissionRequiredMixin, CreateView):
    permission_required = "format.add_time"
    model = Time
    fields = ["format", "code"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context


class TimeList(PermissionRequiredMixin, TemplateView):
    permission_required = "format.view_time"
    template_name = "format/hora_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = ["time_id", "format", "code"]
        model = Time.objects.values_list(*fields)
        context["times"] = modelo_a_tabla_html(model, col_extra=True)
        return context


class TimeDetail(PermissionRequiredMixin, DetailView):
    model = Time
    permission_required = "format.view_time"


class TimeUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "format.change_time"
    model = Time
    fields = ["format", "code"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modify"
        return context


class TimeDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "format.delete_time"
    model = Time
    success_url = reverse_lazy("format:time_index")


#################################################################


class FormatCreate(PermissionRequiredMixin, CreateView):
    model = Format
    fields = [
        "name",
        "description",
        "extension",
        "delimiter",
        "first_row",
        "footer_rows",
        "date_column",
        "date",
        "time_column",
        "time",
        "utc_date",
    ]
    permission_required = "format.add_format"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context


class FormatList(PermissionRequiredMixin, TemplateView):
    template_name = "format/format_list.html"
    permission_required = "format.view_format"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = [
            "format_id",
            "name",
            "description",
            "extension",
            "delimiter",
            "first_row",
            "footer_rows",
            "date_column",
            "date",
            "time_column",
            "time",
            "utc_date",
        ]
        model = Format.objects.values_list(*fields)
        context["format"] = modelo_a_tabla_html(model, col_extra=True)
        return context


class FormatDetail(PermissionRequiredMixin, DetailView):
    permission_required = "format.view_format"
    model = Format

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        variable = Classification.objects.filter(for_id=self.object.for_id)
        context["variable"] = variable
        return context


class FormatUpdate(PermissionRequiredMixin, UpdateView):
    model = Format
    permission_required = "format.change_format"
    fields = [
        "name",
        "description",
        "extension",
        "delimiter",
        "first_row",
        "footer_rows",
        "date_column",
        "date",
        "time_column",
        "time",
        "utc_date",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modify"
        return context


class FormatDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "format.delete_format"
    model = Format
    success_url = reverse_lazy("format:format_index")


# Extension
class ExtensionCreate(PermissionRequiredMixin, CreateView):
    permission_required = "format.add_extension"
    model = Extension
    fields = ["value"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context


class ExtensionList(PermissionRequiredMixin, TemplateView):
    permission_required = "format.view_extension"
    template_name = "format/extension_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = ["extension_id", "value"]
        model = Extension.objects.values_list(*fields)
        context["extension"] = modelo_a_tabla_html(model, col_extra=True)
        return context


class ExtensionUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "format.change_extension"
    model = Extension
    fields = ["value"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modify"
        return context


class ExtensionDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "format.delete_extension"
    model = Extension
    success_url = reverse_lazy("format:extension_index")


# Delimiter
class DelimiterCreate(PermissionRequiredMixin, CreateView):
    permission_required = "format.add_delimiter"
    model = Delimiter
    fields = ["name", "character"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context


class DelimiterList(PermissionRequiredMixin, TemplateView):
    permission_required = "format.view_delimitador"
    template_name = "format/delimiter_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = ["delimiter_id", "name", "character"]
        model = Delimiter.objects.values_list(*fields)
        context["delimiter"] = modelo_a_tabla_html(model, col_extra=True)
        return context


class DelimiterUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "format.change_delimiter"
    model = Delimiter
    fields = ["name", "character"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modify"
        return context


class DelimiterDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "format.delete_delimiter"
    model = Delimiter
    success_url = reverse_lazy("format:delimiter_index")


# Classification
class ClassificationCreate(PermissionRequiredMixin, CreateView):
    permission_required = "format.add_classification"
    model = Classification
    fields = [
        "variable",
        "accumulate",
        "incremental",
        "resolution",
        "decimal_comma",
        "value",
        "value_validator_column",
        "value_validator_text",
        "maximum",
        "maximum_validator_column",
        "maximum_validator_text",
        "minimum",
        "minimum_validator_column",
        "minimum_validator_text",
    ]

    def post(self, request, *args, **kwargs):
        form = ClassificationForm(self.request.POST or None)
        clasificacion = form.save(commit=False)
        format_id = kwargs.get("format_id")
        format = Format.objects.get(format_id=format_id)
        clasificacion.format = format
        clasificacion.save()
        url = reverse("format:format_detail", kwargs={"pk": format.format_id})
        return HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        format_id = kwargs.get("format_id")
        format = Format.objects.get(format_id=format_id)
        context["url"] = reverse(
            "format:clasificacion_create", kwargs={"format": format}
        )
        return context


class ClassificationUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "format.change_classification"
    model = Classification
    fields = [
        "variable",
        "accumulate",
        "incremental",
        "resolution",
        "decimal_comma",
        "value",
        "value_validator_column",
        "value_validator_text",
        "maximum",
        "maximum_validator_column",
        "maximum_validator_text",
        "minimum",
        "minimum_validator_column",
        "minimum_validator_text",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modify"
        cls_id = self.kwargs.get("pk")
        context["url"] = reverse("format:clasificacion_update", kwargs={"pk": cls_id})
        context["format_id"] = self.object.format.format_id
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        format_id = data.get("format_id")
        self.success_url = reverse("format:format_detail", kwargs={"pk": format_id})
        return super().post(data, **kwargs)


class ClassificationDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "format.delete_classification"
    model = Classification

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        format = self.object.format
        self.object.delete()
        return HttpResponseRedirect(
            reverse("format:format_detail", kwargs={"pk": format.format_id})
        )


class ClassificationDetail(PermissionRequiredMixin, DetailView):
    permission_required = "format.view_classification"
    model = Classification


# Association
class AssociationCreate(PermissionRequiredMixin, CreateView):
    permission_required = "format.add_association"
    model = Association
    fields = ["format", "station"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context


class AssociationList(PermissionRequiredMixin, TemplateView):
    permission_required = "format.view_association"
    template_name = "format/association_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = ["association_id", "format__name", "station__station_code"]
        association = Association.objects.all().values_list(*fields)
        context["association"] = modelo_a_tabla_html(association, col_extra=True)
        return context


class AssociationDetail(PermissionRequiredMixin, DetailView):
    permission_required = "format.view_association"
    model = Association


class AssociationUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "format.change_association"
    model = Association
    fields = ["format", "station"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modify"
        return context


class AssociationDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "format.delete_association"
    model = Association
    success_url = reverse_lazy("format:association_index")
