################################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos (iMHEA)
# basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#         Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS), Ecuador.
#         Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones creadoras,
#              ya sea en uso total o parcial del código.

import pandas as pd
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from home.functions import modelo_a_tabla_html

from .forms import *
from .functions import *
from .models import *


class ConsultaForm(PermissionRequiredMixin, TemplateView):
    template_name = "telemetria/visualizar.html"
    permission_required = "telemetria.view_consulta"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tel_est = ConfigVisualizar.objects.values("estacion_id").distinct()
        _modelo = Estacion.objects.filter(pk__in=tel_est)
        campos = [
            "est_id",
            "est_codigo",
            "tipo_id__nombre",
            "est_longitud",
            "est_latitud",
        ]
        df = pd.DataFrame.from_records(
            _modelo.values_list(*campos),
            columns=["id", "Estación", "Tipo", "Longitud", "Latitud"],
        )
        context["estacion"] = df.to_html(header=False, index=False)[47:-18]
        return context


@permission_required("telemetria.view_consulta")
def Consulta(request):
    try:
        estacion_id = int(request.POST.get("estacion", None))
    except ValueError:
        estacion_id = None

    try:
        inicio = request.POST.get("inicio", None)
        if len(inicio) != 10:
            inicio = None
    except ValueError:
        inicio = None

    lista = consulta(estacion_id, inicio)
    return JsonResponse(lista)


class ConsultaCalidadForm(PermissionRequiredMixin, TemplateView):
    template_name = "telemetria/calidad_visualizar.html"
    permission_required = "telemetria.view_calidad_consulta"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tel_est = ConfigCalidad.objects.values("estacion_id").distinct()
        _modelo = Estacion.objects.filter(pk__in=tel_est)
        campos = [
            "est_id",
            "est_codigo",
            "tipo_id__nombre",
            "est_longitud",
            "est_latitud",
        ]
        df = pd.DataFrame.from_records(
            _modelo.values_list(*campos),
            columns=["id", "Estación", "Tipo", "Longitud", "Latitud"],
        )
        context["estacion"] = df.to_html(header=False, index=False)[47:-18]
        return context


@permission_required("telemetria.view_calidad_consulta")
def ConsultaCalidad(request):
    try:
        estacion_id = int(request.POST.get("estacion", None))
    except ValueError:
        estacion_id = None

    try:
        inicio = request.POST.get("inicio", None)
        if len(inicio) != 10:
            inicio = None
    except ValueError:
        inicio = None

    if not request.user.is_authenticated:
        usuario = get_anonymous_user()
    else:
        usuario = request.user
    lista = consulta_calidad(estacion_id, inicio, usuario)
    return JsonResponse(lista)


class ConfigVisualizarList(PermissionRequiredMixin, TemplateView):
    template_name = "telemetria/configvisualizar_list.html"
    permission_required = "telemetria.view_configvisualizar"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = [
            "id",
            "estacion__est_codigo",
            "variable__var_nombre",
            "umbral_superior",
            "umbral_inferior",
        ]
        configvisualizar = ConfigVisualizar.objects.all().values_list(*campos)
        context["configvisualizar"] = modelo_a_tabla_html(
            configvisualizar, col_extra=True
        )
        return context


class ConfigVisualizarDetail(PermissionRequiredMixin, DetailView):
    model = ConfigVisualizar
    permission_required = "telemetria.view_configvisualizar"


class ConfigVisualizarCreate(PermissionRequiredMixin, CreateView):
    model = ConfigVisualizar
    fields = ["estacion", "variable", "umbral_superior", "umbral_inferior"]
    permission_required = "telemetria.add_configvisualizar"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear"
        return context


class ConfigVisualizarUpdate(PermissionRequiredMixin, UpdateView):
    model = ConfigVisualizar
    fields = ["estacion", "variable", "umbral_superior", "umbral_inferior"]
    permission_required = "telemetria.change_configvisualizar"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modificar"
        return context


class ConfigVisualizarDelete(PermissionRequiredMixin, DeleteView):
    model = ConfigVisualizar
    permission_required = "telemetria.delete_configvisualizar"
    success_url = reverse_lazy("telemetria:configvisualizar_list")


class ConfigCalidadList(PermissionRequiredMixin, TemplateView):
    template_name = "telemetria/configcalidad_list.html"
    permission_required = "telemetria.view_configcalidad"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = [
            "id",
            "estacion__est_codigo",
            "variable__var_nombre",
            "profundidad",
            "umbral_superior",
            "umbral_inferior",
        ]
        modelo = ConfigCalidad.objects.all().values_list(*campos)
        context["configcalidad"] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class ConfigCalidadDetail(PermissionRequiredMixin, DetailView):
    model = ConfigCalidad
    permission_required = "telemetria.view_configcalidad"


class ConfigCalidadCreate(PermissionRequiredMixin, CreateView):
    model = ConfigCalidad
    fields = [
        "estacion",
        "variable",
        "profundidad",
        "umbral_superior",
        "umbral_inferior",
    ]
    permission_required = "telemetria.add_configcalidad"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear"
        return context


class ConfigCalidadUpdate(PermissionRequiredMixin, UpdateView):
    model = ConfigCalidad
    fields = [
        "estacion",
        "variable",
        "profundidad",
        "umbral_superior",
        "umbral_inferior",
    ]
    permission_required = "telemetria.change_configcalidad"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modificar"
        return context


class ConfigCalidadDelete(PermissionRequiredMixin, DeleteView):
    model = ConfigCalidad
    permission_required = "telemetria.delete_configcalidad"
    success_url = reverse_lazy("telemetria:configcalidad_list")


#########################


class ConfigAlarmaList(PermissionRequiredMixin, ListView):
    model = AlarmaEmail
    permission_required = "telemetria.view_alarmaemail"
    template_name = "telemetria/alarmaemail_list.html"

    def get_context_data(self, **kwargs):
        context = super(ConfigAlarmaList, self).get_context_data(**kwargs)
        try:
            context["lim_inf_horas"] = TeleVariables.objects.get(
                nombre="ALAR_TRAN_LIMI_INFE"
            ).valor
            context["lim_sup_horas"] = TeleVariables.objects.get(
                nombre="ALAR_TRAN_LIMI_SUPE"
            ).valor
        except TeleVariables.DoesNotExit:
            context["lim_inf_horas"] = None
            context["lim_sup_horas"] = None
        return context


class ConfigAlarmaEmailCreate(PermissionRequiredMixin, CreateView):
    model = AlarmaEmail
    fields = ["email"]
    success_url = reverse_lazy("telemetria:config_alarma_list")
    permission_required = "telemetria.add_alarmaemail"


class ConfigAlarmaEmailDelete(PermissionRequiredMixin, DeleteView):
    model = AlarmaEmail
    success_url = reverse_lazy("telemetria:config_alarma_list")
    permission_required = "telemetria.delete_alarmaemail"


class ConfigAlarmaTransmisionLimites(PermissionRequiredMixin, FormView):
    template_name = "telemetria/config_alarma_transmision_limites.html"
    form_class = AlarmaTransmisionLimitesForm
    success_url = reverse_lazy("telemetria:config_alarma_list")
    permission_required = "telemetria.change_alarmaemail"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if self.request.is_ajax():
            return JsonResponse({"mensaje": "No se admite AJAX"})
        if form.is_valid():
            lim_inf = form.cleaned_data["lim_inf"]
            lim_sup = form.cleaned_data["lim_sup"]
            TeleVariables.objects.update_or_create(
                nombre="ALAR_TRAN_LIMI_INFE", defaults={"valor": lim_inf}
            )
            TeleVariables.objects.update_or_create(
                nombre="ALAR_TRAN_LIMI_SUPE", defaults={"valor": lim_sup}
            )
            return HttpResponseRedirect(reverse_lazy("telemetria:config_alarma_list"))
        else:
            return self.form_invalid(form)


##########################


class MapaTransmision(PermissionRequiredMixin, TemplateView):
    template_name = "telemetria/mapa_transmision.html"
    permission_required = "telemetria.view_mapatransmision"


@permission_required("telemetria.view_mapatransmision")
def MapaTransmisionConsulta(request):
    resultado = consulta_alarma_transmision()
    return JsonResponse(resultado)


############################


class PrecipitacionView(PermissionRequiredMixin, FormView):
    template_name = "telemetria/precipitacion.html"
    form_class = PrecipitacionForm
    permission_required = "telemetria.view_precipitacion"


@permission_required("telemetria.view_precipitacion")
def consulta_precipitacion(request):
    try:
        estacion_id = int(request.POST.get("estacion", None))
    except ValueError:
        estacion_id = None

    try:
        inicio = request.POST.get("inicio", None)
        if len(inicio) != 10:
            inicio = None
    except ValueError:
        inicio = None

    try:
        fin = request.POST.get("fin", None)
        if len(fin) != 10:
            fin = None
    except ValueError:
        fin = None

    lista = datos_precipitacion(estacion_id, inicio, fin)
    return JsonResponse(lista)


class PrecipitacionMultiestacionView(PermissionRequiredMixin, FormView):
    template_name = "telemetria/precipitacion_multiestacion.html"
    form_class = PrecipitacionMultiestacionForm
    permission_required = "telemetria.view_precipitacionmultiestacion"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not self.request.is_ajax():
            return None
        if form.is_valid():
            estaciones = form.cleaned_data["estacion"]
            inicio = form.cleaned_data["inicio"]
            fin = form.cleaned_data["fin"]
            lista = datos_precipitacion_multiestacion(estaciones, inicio, fin)
            return JsonResponse(lista)
        else:
            return JsonResponse({"mensaje": "Formulario no pasó la validación."})
