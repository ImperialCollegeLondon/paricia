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
from django.db import connection
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from rest_framework import generics

import hourly.models as hour
import hourly.serializers as serializers

from .filters import (  # DischargeCurveFilter,; LevelFunctionFilter,; PolarWindFilter,
    HourlyFilter,
    HourlyFilterDepth,
)

# from Hourly.models import DischargeCurve, LevelFunction


# from Hourly.others.functions import level_function_table


class HourlyListBase(generics.ListAPIView):
    """
    Base class for the measurement list views that all use the
    HourlyFilter class to filter the results.
    """

    filterset_class = HourlyFilter


class HourlyDepthListBase(generics.ListAPIView):
    """
    Base class for the measurement list views that all use the
    HourlyFilterDepth class to filter the results.
    """

    filterset_class = HourlyFilterDepth


class PrecipitationList(HourlyListBase):
    """
    List all measurements of Precipitation.
    """

    queryset = hour.Precipitation.objects.all()
    serializer_class = serializers.PrecipitationSerializer


class AirTemperatureList(HourlyListBase):
    """
    List all Hourlys of Air Temperature.
    """

    queryset = hour.AirTemperature.objects.all()
    serializer_class = serializers.AirTemperatureSerializer


class HumidityList(HourlyListBase):
    """
    List all Hourlys of Humidity.
    """

    queryset = hour.Humidity.objects.all()
    serializer_class = serializers.HumiditySerializer


class WindVelocityList(HourlyListBase):
    """
    List all Hourlys of Wind Velocity.
    """

    queryset = hour.WindVelocity.objects.all()
    serializer_class = serializers.WindVelocitySerializer


class WindDirectionList(HourlyListBase):
    """
    List all Hourlys of Wind Direction.
    """

    queryset = hour.WindDirection.objects.all()
    serializer_class = serializers.WindDirectionSerializer


class SoilMoistureList(HourlyListBase):
    """
    List all Hourlys of Soil Moisture.
    """

    queryset = hour.SoilMoisture.objects.all()
    serializer_class = serializers.SoilMoistureSerializer


class SolarRadiationList(HourlyListBase):
    """
    List all Hourlys of Solar Radiation.
    """

    queryset = hour.SolarRadiation.objects.all()
    serializer_class = serializers.SolarRadiationSerializer


class AtmosphericPressureList(HourlyListBase):
    """
    List all Hourlys of Atmospheric Pressure.
    """

    queryset = hour.AtmosphericPressure.objects.all()
    serializer_class = serializers.AtmosphericPressureSerializer


class WaterTemperatureList(HourlyListBase):
    """
    List all Hourlys of Water Temperature.
    """

    queryset = hour.WaterTemperature.objects.all()
    serializer_class = serializers.WaterTemperatureSerializer


class FlowList(HourlyListBase):
    """
    List all Hourlys of Flow.
    """

    queryset = hour.Flow.objects.all()
    serializer_class = serializers.FlowSerializer


class WaterLevelList(HourlyListBase):
    """
    List all Hourlys of Water Level.
    """

    queryset = hour.WaterLevel.objects.all()
    serializer_class = serializers.WaterLevelSerializer


class BatteryVoltageList(HourlyListBase):
    """
    List all Hourlys of Battery Voltage.
    """

    queryset = hour.BatteryVoltage.objects.all()
    serializer_class = serializers.BatteryVoltageSerializer


class FlowManualList(HourlyListBase):
    """
    List all Hourlys of Flow Manual.
    """

    queryset = hour.FlowManual.objects.all()
    serializer_class = serializers.FlowManualSerializer


class StripLevelReadingList(HourlyListBase):
    """
    List all Hourlys of Strip Level Reading.
    """

    queryset = hour.StripLevelReading.objects.all()
    serializer_class = serializers.StripLevelReadingSerializer


class SoilTemperatureList(HourlyListBase):
    """
    List all Hourlys of Soil Temperature.
    """

    queryset = hour.SoilTemperature.objects.all()
    serializer_class = serializers.SoilTemperatureSerializer


class IndirectRadiationList(HourlyListBase):
    """
    List all Hourlys of Indirect Radiation.
    """

    queryset = hour.IndirectRadiation.objects.all()
    serializer_class = serializers.IndirectRadiationSerializer


class WaterTemperatureDepthList(HourlyDepthListBase):
    """
    List all Hourlys of Water Temperature Depth.
    """

    queryset = hour.WaterTemperatureDepth.objects.all()
    serializer_class = serializers.WaterTemperatureDepthSerializer


class WaterAcidityDepthList(HourlyDepthListBase):
    """
    List all Hourlys of Water Acidity Depth.
    """

    queryset = hour.WaterAcidityDepth.objects.all()
    serializer_class = serializers.WaterAcidityDepthSerializer


class RedoxPotentialDepthList(HourlyDepthListBase):
    """
    List all Hourlys of Redox Potential Depth.
    """

    queryset = hour.RedoxPotentialDepth.objects.all()
    serializer_class = serializers.RedoxPotentialDepthSerializer


class WaterTurbidityDepthList(HourlyDepthListBase):
    """
    List all Hourlys of Water Turbidity Depth.
    """

    queryset = hour.WaterTurbidityDepth.objects.all()
    serializer_class = serializers.WaterTurbidityDepthSerializer


class ChlorineConcentrationDepthList(HourlyDepthListBase):
    """
    List all Hourlys of Chlorine Concentration Depth.
    """

    queryset = hour.ChlorineConcentrationDepth.objects.all()
    serializer_class = serializers.ChlorineConcentrationDepthSerializer


class OxygenConcentrationDepthList(HourlyDepthListBase):
    """
    List all Hourlys of Oxygen Concentration Depth.
    """

    queryset = hour.OxygenConcentrationDepth.objects.all()
    serializer_class = serializers.OxygenConcentrationDepthSerializer


class PercentageOxygenConcentrationDepthList(HourlyDepthListBase):
    """
    List all Hourlys of Percentage Oxygen Concentration Depth.
    """

    queryset = hour.PercentageOxygenConcentrationDepth.objects.all()
    serializer_class = serializers.PercentageOxygenConcentrationDepthSerializer


class PhycocyaninDepthList(HourlyDepthListBase):
    """
    List all Hourlys of Phycocyanin Depth.
    """

    queryset = hour.PhycocyaninDepth.objects.all()
    serializer_class = serializers.PhycocyaninDepthSerializer


########################################################################################
# TODO: Revisit theses specialised views that use level_function_table() and create
# Django Rest Framework equivalents.
########################################################################################


# class DischargeCurveDetail(PermissionRequiredMixin, DetailView):
#     model = DischargeCurve
#     permission_required = "Hourly.view_dischargecurve"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         dischargecurve_id = self.object.pk
#         context["levelfunctiontable"] = level_function_table(dischargecurve_id)
#         return context


# class LevelFunctionCreate(PermissionRequiredMixin, CreateView):
#     permission_required = "Hourly.add_dischargecurve"
#     model = LevelFunction
#     form_class = LevelFunctionForm
#
#     def post(self, request, *args, **kwargs):
#         dischargecurve_id = kwargs.get("id")
#         dischargecurve = DischargeCurve.objects.get(pk=dischargecurve_id)
#         form = LevelFunctionForm(self.request.POST or None)
#         try:
#             # Verify if form is correct
#             levelfunction = form.save(commit=False)
#         except Exception:
#             # If it is not, send an informative message.
#             _levelfunctiontable = level_function_table(dischargecurve_id)
#             new_levelfunction = render(
#                 request,
#                 "measurement/levelfunction_form.html",
#                 {"form": LevelFunctionForm(self.request.POST or None)},
#             )
#             return render(
#                 request,
#                 "measurement/dischargecurve_detail.html",
#                 {
#                     "dischargecurve": dischargecurve,
#                     "levelfunctiontable": _levelfunctiontable,
#                     "new_levelfunction": new_levelfunction.content.decode("utf-8"),
#                 },
#             )
#         levelfunction.dischargecurve = dischargecurve
#         levelfunction.save()
#         dischargecurve.requiere_recalculo_caudal = True
#         dischargecurve.save()
#         url = reverse(
#             "measurement:dischargecurve_detail", kwargs={"pk": dischargecurve_id}
#         )
#         return HttpResponseRedirect(url)
#
#     def get_context_data(self, **kwargs):
#         context = super(LevelFunctionCreate, self).get_context_data(**kwargs)
#         context["title"] = "Create"
#         dischargecurve_id = self.kwargs.get("id")
#         context["url"] = reverse(
#             "measurement:levelfunction_create", kwargs={"id": dischargecurve_id}
#         )
#         return context
#
#
# class LevelFunctionUpdate(PermissionRequiredMixin, UpdateView):
#     permission_required = "Hourly.change_dischargecurve"
#     model = LevelFunction
#     fields = ["level", "function"]
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = "Modify"
#         levelfunction_pk = self.kwargs.get("pk")
#         context["url"] = reverse(
#             "measurement:levelfunction_update", kwargs={"pk": levelfunction_pk}
#         )
#         context["dischargecurve_id"] = self.object.dischargecurve.id
#         return context
#
#     def post(self, request, *args, **kwargs):
#         data = request.POST.copy()
#         dischargecurve_id = data.get("dischargecurve_id")
#         dischargecurve = DischargeCurve.objects.get(pk=dischargecurve_id)
#         dischargecurve.require_recalculate_flow = True
#         dischargecurve.save()
#         self.success_url = reverse(
#             "measurement:dischargecurve_detail", kwargs={"pk": dischargecurve_id}
#         )
#         return super().post(data, **kwargs)
#
#
# class LevelFunctionDelete(PermissionRequiredMixin, DeleteView):
#     permission_required = "Hourly.delete_dischargecurve"
#     model = LevelFunction
#
#     def delete(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         dischargecurve = self.object.dischargecurve
#         dischargecurve.require_recalculate_flow = True
#         dischargecurve.save()
#         self.object.delete()
#         return HttpResponseRedirect(
#             reverse(
#                 "measurement:dischargecurve_detail", kwargs={"pk": dischargecurve.id}
#             )
#         )
#
#
# @permission_required("Hourly.add_dischargecurve")
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
