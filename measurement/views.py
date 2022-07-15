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

import measurement.models as meas
import measurement.serializers as serializers
from measurement.models import DischargeCurve, LevelFunction

from .filters import (
    DischargeCurveFilter,
    LevelFunctionFilter,
    MeasurementFilter,
    MeasurementFilterDepth,
    PolarWindFilter,
)
from .forms import LevelFunctionForm
from .functions import level_function_table


class PolarWindList(generics.ListAPIView):
    """
    List all measurements of Polar Wind.
    """

    queryset = meas.PolarWind.objects.all()
    serializer_class = serializers.PolarWindSerializer
    filterset_class = PolarWindFilter


class DischargeCurveList(generics.ListAPIView):
    """
    List all measurements of Discharge Curve.
    """

    queryset = meas.DischargeCurve.objects.all()
    serializer_class = serializers.DischargeCurveSerializer
    filterset_class = DischargeCurveFilter


class LevelFunctionList(generics.ListAPIView):
    """
    List all measurements of Level Function.
    """

    queryset = meas.LevelFunction.objects.all()
    serializer_class = serializers.LevelFunctionSerializer
    filterset_class = LevelFunctionFilter


##############################################################


class MeasurementListBase(generics.ListAPIView):
    """
    Base class for the measurement list views that all use the
    MeasurementFilter class to filter the results.
    """

    filterset_class = MeasurementFilter


class MeasurementDepthListBase(generics.ListAPIView):
    """
    Base class for the measurement list views that all use the
    MeasurementFilterDepth class to filter the results.
    """

    filterset_class = MeasurementFilterDepth


class PrecipitationList(MeasurementListBase):
    """
    List all measurements of Precipitation.
    """

    queryset = meas.Precipitation.objects.all()
    serializer_class = serializers.PrecipitationSerializer


class AirTemperatureList(MeasurementListBase):
    """
    List all measurements of Air Temperature.
    """

    queryset = meas.AirTemperature.objects.all()
    serializer_class = serializers.AirTemperatureSerializer


class HumidityList(MeasurementListBase):
    """
    List all measurements of Humidity.
    """

    queryset = meas.Humidity.objects.all()
    serializer_class = serializers.HumiditySerializer


class WindVelocityList(MeasurementListBase):
    """
    List all measurements of Wind Velocity.
    """

    queryset = meas.WindVelocity.objects.all()
    serializer_class = serializers.WindVelocitySerializer


class WindDirectionList(MeasurementListBase):
    """
    List all measurements of Wind Direction.
    """

    queryset = meas.WindDirection.objects.all()
    serializer_class = serializers.WindDirectionSerializer


class SoilMoistureList(MeasurementListBase):
    """
    List all measurements of Soil Moisture.
    """

    queryset = meas.SoilMoisture.objects.all()
    serializer_class = serializers.SoilMoistureSerializer


class SolarRadiationList(MeasurementListBase):
    """
    List all measurements of Solar Radiation.
    """

    queryset = meas.SolarRadiation.objects.all()
    serializer_class = serializers.SolarRadiationSerializer


class AtmosphericPressureList(MeasurementListBase):
    """
    List all measurements of Atmospheric Pressure.
    """

    queryset = meas.AtmosphericPressure.objects.all()
    serializer_class = serializers.AtmosphericPressureSerializer


class WaterTemperatureList(MeasurementListBase):
    """
    List all measurements of Water Temperature.
    """

    queryset = meas.WaterTemperature.objects.all()
    serializer_class = serializers.WaterTemperatureSerializer


class FlowList(MeasurementListBase):
    """
    List all measurements of Flow.
    """

    queryset = meas.Flow.objects.all()
    serializer_class = serializers.FlowSerializer


class WaterLevelList(MeasurementListBase):
    """
    List all measurements of Water Level.
    """

    queryset = meas.WaterLevel.objects.all()
    serializer_class = serializers.WaterLevelSerializer


class BatteryVoltageList(MeasurementListBase):
    """
    List all measurements of Battery Voltage.
    """

    queryset = meas.BatteryVoltage.objects.all()
    serializer_class = serializers.BatteryVoltageSerializer


class FlowManualList(MeasurementListBase):
    """
    List all measurements of Flow Manual.
    """

    queryset = meas.FlowManual.objects.all()
    serializer_class = serializers.FlowManualSerializer


class StripLevelReadingList(MeasurementListBase):
    """
    List all measurements of Strip Level Reading.
    """

    queryset = meas.StripLevelReading.objects.all()
    serializer_class = serializers.StripLevelReadingSerializer


class SoilTemperatureList(MeasurementListBase):
    """
    List all measurements of Soil Temperature.
    """

    queryset = meas.SoilTemperature.objects.all()
    serializer_class = serializers.SoilTemperatureSerializer


class IndirectRadiationList(MeasurementListBase):
    """
    List all measurements of Indirect Radiation.
    """

    queryset = meas.IndirectRadiation.objects.all()
    serializer_class = serializers.IndirectRadiationSerializer


class WaterTemperatureDepthList(MeasurementDepthListBase):
    """
    List all measurements of Water Temperature Depth.
    """

    queryset = meas.WaterTemperatureDepth.objects.all()
    serializer_class = serializers.WaterTemperatureDepthSerializer


class WaterAcidityDepthList(MeasurementDepthListBase):
    """
    List all measurements of Water Acidity Depth.
    """

    queryset = meas.WaterAcidityDepth.objects.all()
    serializer_class = serializers.WaterAcidityDepthSerializer


class RedoxPotentialDepthList(MeasurementDepthListBase):
    """
    List all measurements of Redox Potential Depth.
    """

    queryset = meas.RedoxPotentialDepth.objects.all()
    serializer_class = serializers.RedoxPotentialDepthSerializer


class WaterTurbidityDepthList(MeasurementDepthListBase):
    """
    List all measurements of Water Turbidity Depth.
    """

    queryset = meas.WaterTurbidityDepth.objects.all()
    serializer_class = serializers.WaterTurbidityDepthSerializer


class ChlorineConcentrationDepthList(MeasurementDepthListBase):
    """
    List all measurements of Chlorine Concentration Depth.
    """

    queryset = meas.ChlorineConcentrationDepth.objects.all()
    serializer_class = serializers.ChlorineConcentrationDepthSerializer


class OxygenConcentrationDepthList(MeasurementDepthListBase):
    """
    List all measurements of Oxygen Concentration Depth.
    """

    queryset = meas.OxygenConcentrationDepth.objects.all()
    serializer_class = serializers.OxygenConcentrationDepthSerializer


class PercentageOxygenConcentrationDepthList(MeasurementDepthListBase):
    """
    List all measurements of Percentage Oxygen Concentration Depth.
    """

    queryset = meas.PercentageOxygenConcentrationDepth.objects.all()
    serializer_class = serializers.PercentageOxygenConcentrationDepthSerializer


class PhycocyaninDepthList(MeasurementDepthListBase):
    """
    List all measurements of Phycocyanin Depth.
    """

    queryset = meas.PhycocyaninDepth.objects.all()
    serializer_class = serializers.PhycocyaninDepthSerializer


########################################################################################
# TODO: Revisit theses specialised views that use level_function_table() and create
# Django Rest Framework equivalents.
########################################################################################


class DischargeCurveDetail(PermissionRequiredMixin, DetailView):
    model = DischargeCurve
    permission_required = "measurement.view_dischargecurve"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dischargecurve_id = self.object.pk
        context["levelfunctiontable"] = level_function_table(dischargecurve_id)
        return context


class LevelFunctionCreate(PermissionRequiredMixin, CreateView):
    permission_required = "measurement.add_dischargecurve"
    model = LevelFunction
    form_class = LevelFunctionForm

    def post(self, request, *args, **kwargs):
        dischargecurve_id = kwargs.get("id")
        dischargecurve = DischargeCurve.objects.get(pk=dischargecurve_id)
        form = LevelFunctionForm(self.request.POST or None)
        try:
            # Verify if form is correct
            levelfunction = form.save(commit=False)
        except Exception:
            # If it is not, send an informative message.
            _levelfunctiontable = level_function_table(dischargecurve_id)
            new_levelfunction = render(
                request,
                "measurement/levelfunction_form.html",
                {"form": LevelFunctionForm(self.request.POST or None)},
            )
            return render(
                request,
                "measurement/dischargecurve_detail.html",
                {
                    "dischargecurve": dischargecurve,
                    "levelfunctiontable": _levelfunctiontable,
                    "new_levelfunction": new_levelfunction.content.decode("utf-8"),
                },
            )
        levelfunction.dischargecurve = dischargecurve
        levelfunction.save()
        dischargecurve.requiere_recalculo_caudal = True
        dischargecurve.save()
        url = reverse(
            "measurement:dischargecurve_detail", kwargs={"pk": dischargecurve_id}
        )
        return HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = super(LevelFunctionCreate, self).get_context_data(**kwargs)
        context["title"] = "Create"
        dischargecurve_id = self.kwargs.get("id")
        context["url"] = reverse(
            "measurement:levelfunction_create", kwargs={"id": dischargecurve_id}
        )
        return context


class LevelFunctionUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "measurement.change_dischargecurve"
    model = LevelFunction
    fields = ["level", "function"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modify"
        levelfunction_pk = self.kwargs.get("pk")
        context["url"] = reverse(
            "measurement:levelfunction_update", kwargs={"pk": levelfunction_pk}
        )
        context["dischargecurve_id"] = self.object.dischargecurve.id
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        dischargecurve_id = data.get("dischargecurve_id")
        dischargecurve = DischargeCurve.objects.get(pk=dischargecurve_id)
        dischargecurve.require_recalculate_flow = True
        dischargecurve.save()
        self.success_url = reverse(
            "measurement:dischargecurve_detail", kwargs={"pk": dischargecurve_id}
        )
        return super().post(data, **kwargs)


class LevelFunctionDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "measurement.delete_dischargecurve"
    model = LevelFunction

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        dischargecurve = self.object.dischargecurve
        dischargecurve.require_recalculate_flow = True
        dischargecurve.save()
        self.object.delete()
        return HttpResponseRedirect(
            reverse(
                "measurement:dischargecurve_detail", kwargs={"pk": dischargecurve.id}
            )
        )


@permission_required("measurement.add_dischargecurve")
def recalculate_flow(request):
    dischargecurve_id = int(request.POST.get("dischargecurve_id", None))
    sql = "SELECT calculate_flow(%s);"
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, [dischargecurve_id])
            cursor.fetchone()
    except Exception:
        result = {"res": False}
        return JsonResponse(result)
    dischargecurve = DischargeCurve.objects.get(pk=dischargecurve_id)
    dischargecurve.require_recalculate_flow = False
    dischargecurve.save()
    result = {"res": True}
    return JsonResponse(result)
