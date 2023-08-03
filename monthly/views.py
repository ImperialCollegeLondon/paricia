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

import daily.models as day
import daily.serializers as serializers

from .filters import (  # DischargeCurveFilter,; LevelFunctionFilter,; PolarWindFilter,
    DailyFilter,
    DailyFilterDepth,
)

# from Daily.models import DischargeCurve, LevelFunction


# from Daily.others.functions import level_function_table


class DailyListBase(generics.ListAPIView):
    """
    Base class for the measurement list views that all use the
    DailyFilter class to filter the results.
    """

    filterset_class = DailyFilter


class DailyDepthListBase(generics.ListAPIView):
    """
    Base class for the measurement list views that all use the
    DailyFilterDepth class to filter the results.
    """

    filterset_class = DailyFilterDepth


class PrecipitationList(DailyListBase):
    """
    List all measurements of Precipitation.
    """

    queryset = day.Precipitation.objects.all()
    serializer_class = serializers.PrecipitationSerializer


class AirTemperatureList(DailyListBase):
    """
    List all Dailys of Air Temperature.
    """

    queryset = day.AirTemperature.objects.all()
    serializer_class = serializers.AirTemperatureSerializer


class HumidityList(DailyListBase):
    """
    List all Dailys of Humidity.
    """

    queryset = day.Humidity.objects.all()
    serializer_class = serializers.HumiditySerializer


class WindVelocityList(DailyListBase):
    """
    List all Dailys of Wind Velocity.
    """

    queryset = day.WindVelocity.objects.all()
    serializer_class = serializers.WindVelocitySerializer


class WindDirectionList(DailyListBase):
    """
    List all Dailys of Wind Direction.
    """

    queryset = day.WindDirection.objects.all()
    serializer_class = serializers.WindDirectionSerializer


class SoilMoistureList(DailyListBase):
    """
    List all Dailys of Soil Moisture.
    """

    queryset = day.SoilMoisture.objects.all()
    serializer_class = serializers.SoilMoistureSerializer


class SolarRadiationList(DailyListBase):
    """
    List all Dailys of Solar Radiation.
    """

    queryset = day.SolarRadiation.objects.all()
    serializer_class = serializers.SolarRadiationSerializer


class AtmosphericPressureList(DailyListBase):
    """
    List all Dailys of Atmospheric Pressure.
    """

    queryset = day.AtmosphericPressure.objects.all()
    serializer_class = serializers.AtmosphericPressureSerializer


class WaterTemperatureList(DailyListBase):
    """
    List all Dailys of Water Temperature.
    """

    queryset = day.WaterTemperature.objects.all()
    serializer_class = serializers.WaterTemperatureSerializer


class FlowList(DailyListBase):
    """
    List all Dailys of Flow.
    """

    queryset = day.Flow.objects.all()
    serializer_class = serializers.FlowSerializer


class WaterLevelList(DailyListBase):
    """
    List all Dailys of Water Level.
    """

    queryset = day.WaterLevel.objects.all()
    serializer_class = serializers.WaterLevelSerializer


class BatteryVoltageList(DailyListBase):
    """
    List all Dailys of Battery Voltage.
    """

    queryset = day.BatteryVoltage.objects.all()
    serializer_class = serializers.BatteryVoltageSerializer


class FlowManualList(DailyListBase):
    """
    List all Dailys of Flow Manual.
    """

    queryset = day.FlowManual.objects.all()
    serializer_class = serializers.FlowManualSerializer


class StripLevelReadingList(DailyListBase):
    """
    List all Dailys of Strip Level Reading.
    """

    queryset = day.StripLevelReading.objects.all()
    serializer_class = serializers.StripLevelReadingSerializer


class SoilTemperatureList(DailyListBase):
    """
    List all Dailys of Soil Temperature.
    """

    queryset = day.SoilTemperature.objects.all()
    serializer_class = serializers.SoilTemperatureSerializer


class IndirectRadiationList(DailyListBase):
    """
    List all Dailys of Indirect Radiation.
    """

    queryset = day.IndirectRadiation.objects.all()
    serializer_class = serializers.IndirectRadiationSerializer


class WaterTemperatureDepthList(DailyDepthListBase):
    """
    List all Dailys of Water Temperature Depth.
    """

    queryset = day.WaterTemperatureDepth.objects.all()
    serializer_class = serializers.WaterTemperatureDepthSerializer


class WaterAcidityDepthList(DailyDepthListBase):
    """
    List all Dailys of Water Acidity Depth.
    """

    queryset = day.WaterAcidityDepth.objects.all()
    serializer_class = serializers.WaterAcidityDepthSerializer


class RedoxPotentialDepthList(DailyDepthListBase):
    """
    List all Dailys of Redox Potential Depth.
    """

    queryset = day.RedoxPotentialDepth.objects.all()
    serializer_class = serializers.RedoxPotentialDepthSerializer


class WaterTurbidityDepthList(DailyDepthListBase):
    """
    List all Dailys of Water Turbidity Depth.
    """

    queryset = day.WaterTurbidityDepth.objects.all()
    serializer_class = serializers.WaterTurbidityDepthSerializer


class ChlorineConcentrationDepthList(DailyDepthListBase):
    """
    List all Dailys of Chlorine Concentration Depth.
    """

    queryset = day.ChlorineConcentrationDepth.objects.all()
    serializer_class = serializers.ChlorineConcentrationDepthSerializer


class OxygenConcentrationDepthList(DailyDepthListBase):
    """
    List all Dailys of Oxygen Concentration Depth.
    """

    queryset = day.OxygenConcentrationDepth.objects.all()
    serializer_class = serializers.OxygenConcentrationDepthSerializer


class PercentageOxygenConcentrationDepthList(DailyDepthListBase):
    """
    List all Dailys of Percentage Oxygen Concentration Depth.
    """

    queryset = day.PercentageOxygenConcentrationDepth.objects.all()
    serializer_class = serializers.PercentageOxygenConcentrationDepthSerializer


class PhycocyaninDepthList(DailyDepthListBase):
    """
    List all Dailys of Phycocyanin Depth.
    """

    queryset = day.PhycocyaninDepth.objects.all()
    serializer_class = serializers.PhycocyaninDepthSerializer


########################################################################################
# TODO: Revisit theses specialised views that use level_function_table() and create
# Django Rest Framework equivalents.
########################################################################################


# class DischargeCurveDetail(PermissionRequiredMixin, DetailView):
#     model = DischargeCurve
#     permission_required = "Daily.view_dischargecurve"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         dischargecurve_id = self.object.pk
#         context["levelfunctiontable"] = level_function_table(dischargecurve_id)
#         return context


# class LevelFunctionCreate(PermissionRequiredMixin, CreateView):
#     permission_required = "Daily.add_dischargecurve"
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
#     permission_required = "Daily.change_dischargecurve"
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
#     permission_required = "Daily.delete_dischargecurve"
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
# @permission_required("Daily.add_dischargecurve")
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
