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

from django.apps import apps
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import connection
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from rest_framework import generics

# from .forms import LevelFunctionForm
# from validated.others.functions import level_function_table
import validated.functions as functions
import validated.models as vali
import validated.serializers as serializers
from station.models import Station

from .filters import (  # DischargeCurveFilter,; LevelFunctionFilter,; PolarWindFilter,
    ValidatedFilter,
    ValidatedFilterDepth,
)

# from validated.models import DischargeCurve, LevelFunction


# class PolarWindList(generics.ListAPIView):
#     """
#     List all measurements of Polar Wind.
#     """
#
#     queryset = vali.PolarWind.objects.all()
#     serializer_class = serializers.PolarWindSerializer
#     filterset_class = PolarWindFilter


class ValidatedListBase(generics.ListAPIView):
    """
    Base class for the measurement list views that all use the
    ValidatedFilter class to filter the results.
    """

    filterset_class = ValidatedFilter


class ValidatedDepthListBase(generics.ListAPIView):
    """
    Base class for the measurement list views that all use the
    ValidatedFilterDepth class to filter the results.
    """

    filterset_class = ValidatedFilterDepth


class PrecipitationList(ValidatedListBase):
    """
    List all measurements of Precipitation.
    """

    queryset = vali.Precipitation.objects.all()
    serializer_class = serializers.PrecipitationSerializer


class AirTemperatureList(ValidatedListBase):
    """
    List all validateds of Air Temperature.
    """

    queryset = vali.AirTemperature.objects.all()
    serializer_class = serializers.AirTemperatureSerializer


class HumidityList(ValidatedListBase):
    """
    List all validateds of Humidity.
    """

    queryset = vali.Humidity.objects.all()
    serializer_class = serializers.HumiditySerializer


class WindVelocityList(ValidatedListBase):
    """
    List all validateds of Wind Velocity.
    """

    queryset = vali.WindVelocity.objects.all()
    serializer_class = serializers.WindVelocitySerializer


class WindDirectionList(ValidatedListBase):
    """
    List all validateds of Wind Direction.
    """

    queryset = vali.WindDirection.objects.all()
    serializer_class = serializers.WindDirectionSerializer


class SoilMoistureList(ValidatedListBase):
    """
    List all validateds of Soil Moisture.
    """

    queryset = vali.SoilMoisture.objects.all()
    serializer_class = serializers.SoilMoistureSerializer


class SolarRadiationList(ValidatedListBase):
    """
    List all validateds of Solar Radiation.
    """

    queryset = vali.SolarRadiation.objects.all()
    serializer_class = serializers.SolarRadiationSerializer


class AtmosphericPressureList(ValidatedListBase):
    """
    List all validateds of Atmospheric Pressure.
    """

    queryset = vali.AtmosphericPressure.objects.all()
    serializer_class = serializers.AtmosphericPressureSerializer


class WaterTemperatureList(ValidatedListBase):
    """
    List all validateds of Water Temperature.
    """

    queryset = vali.WaterTemperature.objects.all()
    serializer_class = serializers.WaterTemperatureSerializer


class FlowList(ValidatedListBase):
    """
    List all validateds of Flow.
    """

    queryset = vali.Flow.objects.all()
    serializer_class = serializers.FlowSerializer


class WaterLevelList(ValidatedListBase):
    """
    List all validateds of Water Level.
    """

    queryset = vali.WaterLevel.objects.all()
    serializer_class = serializers.WaterLevelSerializer


class BatteryVoltageList(ValidatedListBase):
    """
    List all validateds of Battery Voltage.
    """

    queryset = vali.BatteryVoltage.objects.all()
    serializer_class = serializers.BatteryVoltageSerializer


class FlowManualList(ValidatedListBase):
    """
    List all validateds of Flow Manual.
    """

    queryset = vali.FlowManual.objects.all()
    serializer_class = serializers.FlowManualSerializer


class StripLevelReadingList(ValidatedListBase):
    """
    List all validateds of Strip Level Reading.
    """

    queryset = vali.StripLevelReading.objects.all()
    serializer_class = serializers.StripLevelReadingSerializer


class SoilTemperatureList(ValidatedListBase):
    """
    List all validateds of Soil Temperature.
    """

    queryset = vali.SoilTemperature.objects.all()
    serializer_class = serializers.SoilTemperatureSerializer


class IndirectRadiationList(ValidatedListBase):
    """
    List all validateds of Indirect Radiation.
    """

    queryset = vali.IndirectRadiation.objects.all()
    serializer_class = serializers.IndirectRadiationSerializer


class WaterTemperatureDepthList(ValidatedDepthListBase):
    """
    List all validateds of Water Temperature Depth.
    """

    queryset = vali.WaterTemperatureDepth.objects.all()
    serializer_class = serializers.WaterTemperatureDepthSerializer


class WaterAcidityDepthList(ValidatedDepthListBase):
    """
    List all validateds of Water Acidity Depth.
    """

    queryset = vali.WaterAcidityDepth.objects.all()
    serializer_class = serializers.WaterAcidityDepthSerializer


class RedoxPotentialDepthList(ValidatedDepthListBase):
    """
    List all validateds of Redox Potential Depth.
    """

    queryset = vali.RedoxPotentialDepth.objects.all()
    serializer_class = serializers.RedoxPotentialDepthSerializer


class WaterTurbidityDepthList(ValidatedDepthListBase):
    """
    List all validateds of Water Turbidity Depth.
    """

    queryset = vali.WaterTurbidityDepth.objects.all()
    serializer_class = serializers.WaterTurbidityDepthSerializer


class ChlorineConcentrationDepthList(ValidatedDepthListBase):
    """
    List all validateds of Chlorine Concentration Depth.
    """

    queryset = vali.ChlorineConcentrationDepth.objects.all()
    serializer_class = serializers.ChlorineConcentrationDepthSerializer


class OxygenConcentrationDepthList(ValidatedDepthListBase):
    """
    List all validateds of Oxygen Concentration Depth.
    """

    queryset = vali.OxygenConcentrationDepth.objects.all()
    serializer_class = serializers.OxygenConcentrationDepthSerializer


class PercentageOxygenConcentrationDepthList(ValidatedDepthListBase):
    """
    List all validateds of Percentage Oxygen Concentration Depth.
    """

    queryset = vali.PercentageOxygenConcentrationDepth.objects.all()
    serializer_class = serializers.PercentageOxygenConcentrationDepthSerializer


class PhycocyaninDepthList(ValidatedDepthListBase):
    """
    List all validateds of Phycocyanin Depth.
    """

    queryset = vali.PhycocyaninDepth.objects.all()
    serializer_class = serializers.PhycocyaninDepthSerializer


########################################################################################
# TODO: Revisit theses specialised views that use level_function_table() and create
# Django Rest Framework equivalents.
########################################################################################


#
# @permission_required("validated.add_dischargecurve")
# def recalculate_flow(request):
#     dischargecurve_id = int(request.POST.get("dischargecurve_id", None))
#     sql = "SELECT calculate_flow(%s);"
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute(sql, [dischargecurve_id])
#             cursor.fetchone()
#     except Exception:
#         result = {"res": False}
#         return JsonResponse(result)
#     dischargecurve = DischargeCurve.objects.get(pk=dischargecurve_id)
#     dischargecurve.require_recalculate_flow = False
#     dischargecurve.save()
#     result = {"res": True}
#     return JsonResponse(result)


# from val2 import functions
import json
from datetime import datetime, time

import pandas as pd
from django.contrib.auth.decorators import permission_required

# from medicion.forms import ValidacionSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection

# from medicion.models import *
from django.db.models import Max, Min
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import FormView, ListView

# from threading import Thread
# from validacion.serializers import *
from rest_framework.generics import ListAPIView

# from val2.forms import BorrarForm
# from validacion import functions as funcvariable
from variable.models import Variable

from .forms import DailyValidationForm

# from estacion.views import listar_anio
# from val2.functions import guardar_cambios_validacion


class DailyValidation(FormView):
    template_name = "daily_validation.html"
    form_class = DailyValidationForm
    success_url = "/validated/daily_validation/"

    def post(self, request, *args, **kwargs):
        form = DailyValidationForm(self.request.POST or None)
        if form.is_valid():
            if self.request.is_ajax():
                variable = form.cleaned_data["variable"]
                station = form.cleaned_data["station"]
                start_date = form.cleaned_data["start_date"]
                end_date = form.cleaned_data["end_date"]
                maximum = form.cleaned_data["maximum"]
                minimum = form.cleaned_data["minimum"]
                data = functions.daily_validation(
                    station, variable, start_date, end_date, minimum, maximum
                )
                data_json = json.dumps(data, allow_nan=True, cls=DjangoJSONEncoder)
                return HttpResponse(data_json, content_type="application/json")

        return render(request, "home/form_error.html", {"form": form})


# Consulta de datos crudos y/o validados por estacion, variable y hora
class DetailList(ListView):
    template_name = "home/message.html"

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            station_id = kwargs.get("station_id")
            variable_id = kwargs.get("variable_id")
            date = kwargs.get("date")
            minimum = kwargs.get("minimum")
            maximum = kwargs.get("maximum")

            datos = functions.detail_list(
                station_id, variable_id, date, minimum, maximum
            )
            data_json = json.dumps(datos, allow_nan=True, cls=DjangoJSONEncoder)
            return HttpResponse(data_json, content_type="application/json")
        message = "Ocurrio un problema con el procesamiento de la información, por favor contacte con el administrador"
        return render(request, "home/message.html", {"message": message})


# Pasar los datos crudos a validados
def daily_save(request):
    station_id = int(request.POST.get("station_id", None))
    variable_id = int(request.POST.get("variable_id", None))
    maximum = float(request.POST.get("maximum", None))
    minimum = float(request.POST.get("minimum", None))
    changes_json = request.POST.get("changes", None)

    station = Station.objects.get(station_id=station_id)
    variable = Variable.objects.get(variable_id=variable_id)
    changes_list = json.loads(changes_json)

    conditions = functions.get_conditions(changes_list)

    result = functions.save_to_validated(
        changes_list,
        variable,
        station,
        conditions,
        minimum,
        maximum,
    )
    if result:
        list = {"result": result}
    else:
        list = {"result": False}
    return JsonResponse(list)


def detail_save(request):
    station_id = int(request.POST.get("station_id", None))
    variable_id = int(request.POST.get("variable_id", None))
    data_json = request.POST.get("data", None)

    variable = Variable.objects.get(variable_id=variable_id)
    station = Station.objects.get(station_id=station_id)
    data_list = json.loads(data_json)

    fecha_inicio_dato = data_list[0]["fecha"]
    fecha_fin_dato = data_list[-1]["fecha"]

    # Delete previous validation
    Validated = apps.get_model(app_label="validated", model_name=variable.variable_code)
    Validated.timescale.filter(
        time__range=[fecha_inicio_dato, fecha_fin_dato],
        station_id=station.station_id,
    ).delete()

    # Insert new validation using postgres function: insertar_$var_name$_validacion'
    #            insertion script defined insertar_validaicion_pro.sql
    #     cursor.callproc('insertar_' + variable.var_modelo.lower() + '_validacion', [estacion_id, cambios_json])

    model_instances = []
    for row in data_list:
        if not row["seleccionado"]:
            continue

        if not row["estado"]:
            row["valor"] = None
            row["maximo"] = None
            row["minimo"] = None
        # TODO ask if the following else condition has any sense
        # else:
        #     row["maximo"] = row["maximo"] if row["maximo"] is not None else row["valor"]
        #     row["minimo"] = row["minimo"] if row["minimo"] is not None else row["valor"]

        model_instances.append(
            Validated(
                time=row["fecha"],
                value=row["valor"],
                maximum=row["maximo"],
                minimum=row["minimo"],
                station_id=station.station_id,
            )
        )

    insert_result = Validated.objects.bulk_create(model_instances)
    result = False
    if len(insert_result) == len(model_instances):
        result = True

    # if resultado:
    #     lista = {'resultado': resultado}
    #     fecha_inicio = cambios_lista[0]['fecha']
    #     fecha_fin = cambios_lista[-1]['fecha']
    #     t = Thread(target=guardar_cambios_validacion, args=(estacion_id, variable, 'insert', fecha_inicio, fecha_fin))
    #     t.start()
    # else:
    #     lista = {'resultado': False}
    # print(resultado)
    return JsonResponse({"resultado": result})


#
# # Consular los periodos de validacion por estacion y variable
# class PeriodosValidacion(PermissionRequiredMixin, FormView):
#     template_name = 'validacion_v2/periodos_validacion.html'
#     form_class = ValidacionSearchForm
#     success_url = '/medicion/filter/'
#     permission_required = 'validacion_v2.validacion_diaria'
#     lista = []
#
#     def post(self, request, *args, **kwargs):
#         estacion_id = None
#         variable_id = None
#         try:
#             estacion_id = int(request.POST.get('estacion', None))
#             variable_id = int(request.POST.get('variable', None))
#             print(estacion_id)
#             inicio = request.POST.get('inicio', None)
#             variable = Variable.objects.get(var_id=variable_id)
#             modelo = variable.var_modelo.lower()
#         except:
#             pass
#
#         intervalos = functions.periodos_validacion(est_id=estacion_id, variable=variable, inicio=inicio)
#         return render(request, self.template_name, {'intervalos': intervalos})
#
#
# # TODO: Revisar el funcionamiento de esta vista
# class ValidacionBorrar(PermissionRequiredMixin, FormView):
#     template_name = 'validacion/borrar.html'
#     form_class = BorrarForm
#     success_url = '/validacion/borrar/'
#     permission_required = 'validacion_v2.validacion_diaria'
#     resultado = None
#
#     def form_valid(self, form):
#         estacion_id = form.cleaned_data['estacion'].est_id
#         variable = form.cleaned_data['variable']
#         inicio = form.cleaned_data['inicio']
#         fin = form.cleaned_data['fin']
#
#         filas_validado = 0
#         sql = "DELETE FROM validacion_var%%var_id%%validado WHERE estacion_id = %s AND fecha >= %s AND fecha <= %s;"
#         if variable.var_id == 4 or variable.var_id == 5:
#             sql = """DELETE FROM validacion_viento WHERE estacion_id = %s AND fecha >= %s AND fecha <= %s;
#             DELETE FROM validacion_var4validado WHERE estacion_id = %s AND fecha >= %s AND fecha <= %s;
#             DELETE FROM validacion_var5validado WHERE estacion_id = %s AND fecha >= %s AND fecha <= %s;
#             """
#
#         sql = sql.replace('%%var_id%%', str(variable.var_id))
#         with connection.cursor() as cursor:
#             cursor.execute(sql, [estacion_id, inicio, fin])
#             filas_validado = cursor.rowcount
#
#         filas_horario = 0
#         sql = "DELETE FROM horario_var%%var_id%%horario WHERE estacion_id = %s AND fecha >= date_trunc('hour', %s) AND fecha <= date_trunc('hour', %s);"
#         if variable.var_id == 4 or variable.var_id == 5:
#             sql = """DELETE FROM horario_var4horario WHERE estacion_id = %s AND fecha >= date_trunc('hour', %s) AND fecha <= date_trunc('hour', %s);
#             DELETE FROM horario_var5horario WHERE estacion_id = %s AND fecha >= date_trunc('hour', %s) AND fecha <= date_trunc('hour', %s);"""
#
#         sql = sql.replace('%%var_id%%', str(variable.var_id))
#         with connection.cursor() as cursor:
#             cursor.execute(sql, [estacion_id, inicio, fin])
#             filas_horario = cursor.rowcount
#
#         filas_diario = 0
#         sql = "DELETE FROM diario_var%%var_id%%diario WHERE estacion_id = %s AND fecha >= date_trunc('day', %s) AND fecha <= date_trunc('day', %s);"
#         if variable.var_id == 4 or variable.var_id == 5:
#             sql = """DELETE FROM diario_var4diario WHERE estacion_id = %s AND fecha >= date_trunc('hour', %s) AND fecha <= date_trunc('hour', %s);
#             DELETE FROM diario_var5diario WHERE estacion_id = %s AND fecha >= date_trunc('hour', %s) AND fecha <= date_trunc('hour', %s);"""
#
#         sql = sql.replace('%%var_id%%', str(variable.var_id))
#         with connection.cursor() as cursor:
#             cursor.execute(sql, [estacion_id, inicio, fin])
#             filas_diario = cursor.rowcount
#
#         filas_mensual = 0
#         sql = "DELETE FROM mensual_var%%var_id%%mensual WHERE estacion_id = %s AND fecha >= date_trunc('month', %s) AND fecha <= date_trunc('month', %s);"
#         if variable.var_id == 4 or variable.var_id == 5:
#             sql = """DELETE FROM mensual_var4mensual WHERE estacion_id = %s AND fecha >= date_trunc('hour', %s) AND fecha <= date_trunc('hour', %s);
#             DELETE FROM mensual_var5mensual WHERE estacion_id = %s AND fecha >= date_trunc('hour', %s) AND fecha <= date_trunc('hour', %s);"""
#
#         sql = sql.replace('%%var_id%%', str(variable.var_id))
#         with connection.cursor() as cursor:
#             cursor.execute(sql, [estacion_id, inicio, fin])
#             filas_mensual = cursor.rowcount
#
#         if self.request.is_ajax():
#             data = {
#                 'filas_validado': filas_validado,
#                 'filas_horario': filas_horario,
#                 'filas_diario': filas_diario,
#                 'filas_mensual': filas_mensual
#             }
#             cursor.close()
#             return JsonResponse(data)
#         else:
#             cursor.close()
#             return super().form_valid(form)
#
#


# # Pasar los datos crudos a validados
# @permission_required('validacion_v2.validacion_diaria')
# def guardar_validados(request):
#     # Verificando datos json para evitar inyeccion SQL
#     estacion_id = int(request.POST.get('estacion_id', None))
#     variable_id = int(request.POST.get('variable_id', None))
#     limite_superior = float(request.POST.get('limite_superior', None))
#     limite_inferior = float(request.POST.get('limite_inferior', None))
#     cambios_json = request.POST.get('cambios', None)
#
#     variable = Variable.objects.get(var_id=variable_id)
#     cambios_lista = json.loads(cambios_json)
#
#     condiciones = functions.get_condiciones(cambios_lista)
#
#     resultado = functions.pasar_crudos_validados(cambios_lista, variable, estacion_id,
#                                                  condiciones, limite_superior, limite_inferior)
#
#     if resultado:
#         fecha_inicio = cambios_lista[0]['fecha']
#         fecha_fin = cambios_lista[-1]['fecha']
#         lista = {'resultado': resultado}
#         t = Thread(target=guardar_cambios_validacion, args=(estacion_id, variable, 'insert', fecha_inicio, fecha_fin))
#         t.start()
#
#     else:
#         lista = {'resultado': False}
#
#     return JsonResponse(lista)


# # Permite eliminar los datos validados
# @permission_required('validacion_v2.validacion_diaria')
# def eliminar_validados(request):
#     estacion_id = int(request.POST.get('estacion_id', None))
#     variable_id = int(request.POST.get('variable_id', None))
#     cambios_json = request.POST.get('cambios', None)
#
#     variable = Variable.objects.get(var_id=variable_id)
#
#     cambios_lista = json.loads(cambios_json)
#     condiciones = functions.get_condiciones(cambios_lista)
#     resultado = functions.eliminar_datos_validacion(cambios_lista, variable, estacion_id, condiciones)
#     lista = {'resultado': resultado}
#     fecha_inicio = cambios_lista[0]['fecha']
#     fecha_fin = cambios_lista[-1]['fecha']
#     t = Thread(target=guardar_cambios_validacion, args=(estacion_id, variable, 'delete', fecha_inicio, fecha_fin))
#     t.start()
#
#     return JsonResponse(lista)
#
#
# # La funcion esta duplicada
# '''def eliminar_validados(request):
#     estacion_id = int(request.POST.get('estacion_id', None))
#     variable_id = int(request.POST.get('variable_id', None))
#     cambios_json = request.POST.get('cambios', None)
#
#     variable = Variable.objects.get(var_id=variable_id)
#
#     cambios_lista = json.loads(cambios_json)
#     condiciones = functions.get_condiciones(cambios_lista)
#     resultado = functions.eliminar_datos_validacion(cambios_lista, variable, estacion_id, condiciones)
#     lista = {'resultado': resultado}
#
#     return JsonResponse(lista)'''
#
#
# class ValidacionList(PermissionRequiredMixin, FormView):
#     template_name = 'validacion_v2/periodos_validacion.html'
#     permission_required = 'validacion_v2.validacion_diaria'
#     form_class = ValidacionSearchForm
#     success_url = '/medicion/filter/'
#     lista = []
#
#     def post(self, request, *args, **kwargs):
#         estacion_id = None
#         variable_id = None
#         try:
#             estacion_id = int(request.POST.get('estacion', None))
#             variable_id = int(request.POST.get('variable', None))
#             m = 'Var' + str(variable_id) + 'Medicion'
#             m = globals()[m]
#             fechaa = m.objects.filter(estacion_id__exact=estacion_id).aggregate(Max('fecha'), Min('fecha'))
#             # print(fechaa['fecha__min'])
#             inicio = str(fechaa['fecha__min'])
#             # print(inicio)
#             variable = Variable.objects.get(var_id=variable_id)
#             # res = variable.var_modelo.lower()
#         except:
#             pass
#
#         intervalos = functions.periodos_validacion2(estacion_id, variable, inicio)
#         return render(request, self.template_name, {'intervalos': intervalos})
