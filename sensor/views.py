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
from sensor.models import Sensor, SensorBrand, SensorType


class SensorList(PermissionRequiredMixin, TemplateView):
    template_name = "sensor/sensor_list.html"
    permission_required = "sensor.view_sensor"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = [
            "sensor_id",
            "code",
            "sensor_type__name",
            "sensor_brand__name",
            "model",
            "serial",
            "status",
        ]
        modelo = Sensor.objects.values_list(*campos)
        context["sensores"] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class SensorCreate(PermissionRequiredMixin, CreateView):
    model = Sensor
    permission_required = "sensor.add_sensor"
    fields = [
        "code",
        "sensor_type",
        "sensor_brand",
        "model",
        "serial",
        "status",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context


class SensorDetail(PermissionRequiredMixin, DetailView):
    model = Sensor
    permission_required = "sensor.view_sensor"


class SensorUpdate(PermissionRequiredMixin, UpdateView):
    model = Sensor
    permission_required = "sensor.change_sensor"
    fields = [
        "code",
        "sensor_type",
        "sensor_brand",
        "model",
        "serial",
        "status",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update"
        return context


class SensorDelete(PermissionRequiredMixin, DeleteView):
    model = Sensor
    permission_required = "sensor.delete_sensor"
    success_url = reverse_lazy("sensor:sensor_index")


@permission_required("sensor.view_sensor")
def SensorExport(request):
    if request.user.is_authenticated:
        cabecera = [
            ["Code", "Type", "Brand", "Model", "Serial"],
        ]
        cuerpo = []
        objetos = Sensor.objects.all()
        for objeto in objetos:
            fila = []
            fila.append(objeto.code)
            fila.append(
                objeto.sensor_type.name if objeto.sensor_type is not None else None
            )
            fila.append(
                objeto.sensor_brand.brand if objeto.sensor_brand is not None else None
            )
            fila.append(objeto.model)
            fila.append(objeto.serial)
            cuerpo.append(fila)
        response = ExcelResponse(cabecera + cuerpo, "Sensores_iMHEA")
        return response


@permission_required("sensor.view_sensor")
def ListaSensores(request):
    sensores = Sensor.objects.all()
    lista = []
    for row in sensores:
        linea = row.code + " -- " + ("" if row.model is None else row.model + " - ")
        lista.append(linea)
    return JsonResponse({"lista": lista})


# #  MARCA


class SensorBrandList(PermissionRequiredMixin, TemplateView):
    template_name = "sensor/brand_list.html"
    permission_required = "sensor.view_brand"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = [
            "brand_id",
            "name",
        ]
        modelo = SensorBrand.objects.values_list(*campos)
        context["brands"] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class SensorBrandCreate(PermissionRequiredMixin, CreateView):
    model = SensorBrand
    permission_required = "sensor.add_brand"
    fields = ["name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context


class SensorBrandDetail(PermissionRequiredMixin, DetailView):
    model = SensorBrand
    permission_required = "sensor.view_brand"


class SensorBrandUpdate(PermissionRequiredMixin, UpdateView):
    model = SensorBrand
    permission_required = "sensor.change_brand"
    fields = ["brand"]

    def get_context_data(self, **kwargs):
        context = super(SensorBrandUpdate, self).get_context_data(**kwargs)
        context["title"] = "Update"
        return context


class SensorBrandDelete(PermissionRequiredMixin, DeleteView):
    model = SensorBrandUpdate
    permission_required = "sensor.delete_brand"
    success_url = reverse_lazy("sensor:brand_index")


# SensorType
class SensorTypeList(PermissionRequiredMixin, TemplateView):
    template_name = "sensor/type_list.html"
    permission_required = "sensor.view_type"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = [
            "sensor_type",
            "name",
        ]
        modelo = SensorType.objects.values_list(*campos)
        context["type"] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class SensorTypeCreate(PermissionRequiredMixin, CreateView):
    model = SensorType
    permission_required = "sensor.add_type"
    fields = ["name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context


class SensorTypeDetail(PermissionRequiredMixin, DetailView):
    model = SensorType
    permission_required = "sensor.view_type"


class SensorTypeUpdate(PermissionRequiredMixin, UpdateView):
    model = SensorType
    permission_required = "sensor.change_type"
    fields = ["name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update"
        return context


class SensorTypeDelete(PermissionRequiredMixin, DeleteView):
    model = SensorType
    permission_required = "sensor.delete_type"
    success_url = reverse_lazy("sensor:type_index")
