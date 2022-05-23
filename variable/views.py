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

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from excel_response import ExcelResponse

from home.functions import modelo_a_tabla_html

from .models import SensorInstallation, Unit, Variable


class VariableCreate(PermissionRequiredMixin, CreateView):
    model = Variable
    permission_required = "variable.__super__add_variable"
    fields = [
        "variable_code",
        "name",
        "unit",
        "maximum",
        "minimum",
        # TODO: update these
        "var_sos",
        "var_err",
        "var_min",
        "var_estado",
        "is_cumulative",
        "automatic_report",
        "vacios",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context


class VariableList(PermissionRequiredMixin, TemplateView):
    template_name = "variable/variable_list.html"
    permission_required = "variable.view_variable"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = [
            "variable_code",
            "name",
            "unit",
            "maximum",
            "minimum",
            # TODO: update these
            "var_sos",
            "var_err",
            "var_min",
            "var_estado",
            "is_cumulative",
            "automatic_report",
            "vacios",
        ]
        modelo = Variable.objects.values_list(*fields)
        context["variables"] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class VariableDetail(PermissionRequiredMixin, DetailView):
    model = Variable
    permission_required = "variable.view_variable"


class VariableUpdate(PermissionRequiredMixin, UpdateView):
    model = Variable
    permission_required = "variable.change_variable"
    fields = [
        "variable_code",
        "name",
        "unit",
        "maximum",
        "minimum",
        # TODO: update these
        "var_sos",
        "var_err",
        "var_min",
        "var_estado",
        "is_cumulative",
        "automatic_report",
        "vacios",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modify"
        return context


class VariableDelete(PermissionRequiredMixin, DeleteView):
    model = Variable
    permission_required = "variable.__super__delete_variable"
    success_url = reverse_lazy("variable:variable_index")


@permission_required("variable.view_variable")
def VariableExport(request):
    header = [
        ["Code", "Name", "Unit"],
    ]
    body = []
    objects = Variable.objects.all()
    for obj in objects:
        line = []
        line.append(obj.code)
        line.append(obj.name)
        try:
            line.append("' " + obj.unit.initials)
        # TODO fix bare except
        except:
            line.append(None)
        body.append(line)
    response = ExcelResponse(header + body, "Variables_iMHEA")
    return response


##################################################################
# Unit
class UnitCreate(PermissionRequiredMixin, CreateView):
    model = Unit
    permission_required = "variable.add_unit"
    fields = ["name", "initials"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context


class UnitList(PermissionRequiredMixin, TemplateView):
    template_name = "variable/unit_list.html"
    permission_required = "variable.view_unit"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = ["unit_id", "name", "initials"]
        model = Unit.objects.values_list(*fields)
        context["units"] = modelo_a_tabla_html(model, col_extra=True)
        return context


class UnitDetail(PermissionRequiredMixin, DetailView):
    model = Unit
    permission_required = "variable.view_unit"


class UnitUpdate(PermissionRequiredMixin, UpdateView):
    model = Unit
    permission_required = "variable.change_unit"
    fields = ["name", "initials"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modify"
        return context


class UnidadDelete(PermissionRequiredMixin, DeleteView):
    model = Unit
    permission_required = "variable.delete_unit"
    success_url = reverse_lazy("variable:unit_index")


####################################################################
# Model Control
class SensorInstallationCreate(PermissionRequiredMixin, CreateView):
    model = SensorInstallation
    permission_required = "variable.add_sensorinstallation"
    fields = [
        "variable",
        "sensor",
        "station",
        "start_date",
        "end_date",
        "state",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context


class SensorInstallationList(PermissionRequiredMixin, TemplateView):
    template_name = "variable/sensorinstallation_list.html"
    permission_required = "variable.view_sensorinstallation"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = [
            "sensorinstallation_id",
            "variable__name",
            "sensor__code",
            "station__station_code",
            "start_date",
            "end_date",
            "state",
        ]
        model = SensorInstallation.objects.all().values_list(*fields)
        context["sensor_installation"] = modelo_a_tabla_html(model, col_extra=True)
        return context


class SensorInstallationDetail(PermissionRequiredMixin, DetailView):
    model = SensorInstallation
    permission_required = "variable.view_sensorinstallation"


class SensorInstallationUpdate(PermissionRequiredMixin, UpdateView):
    model = SensorInstallation
    permission_required = "variable.change_sensorinstallation"
    fields = [
        "variable",
        "sensor",
        "station",
        "start_date",
        "end_date",
        "state",
    ]

    def get_context_data(self, **kwargs):
        context = super(SensorInstallationUpdate, self).get_context_data(**kwargs)
        context["title"] = "Modify"
        return context


class SensorInstallationDelete(PermissionRequiredMixin, DeleteView):
    model = SensorInstallation
    permission_required = "variable.delete_sensorinstallation"
    success_url = reverse_lazy("variable:sensorinstallation_index")


def get_limits(request):
    print(request.POST.get("variable_id"))
    id = int(request.POST.get("variable_id"))
    variable = Variable.objects.get(variable_id=id)
    data = {"maximum": variable.maximum, "minimum": variable.minimum}
    return JsonResponse(data)
