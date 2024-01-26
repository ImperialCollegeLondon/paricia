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

import json
from datetime import datetime
from decimal import Decimal

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import FormView, ListView
from rest_framework import generics

import validated.functions as functions
import validated.models as vali
import validated.serializers as serializers
from station.models import Station
from variable.models import Variable

from .filters import (  # DischargeCurveFilter,; LevelFunctionFilter,; PolarWindFilter,
    ValidatedFilter,
    ValidatedFilterDepth,
)
from .forms import DailyValidationForm, DataReportForm

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


class DailyValidation(FormView):
    """
    Main form to perform data validation
    Select variable, station, and dates, and the system shows a table with indicators.
    Once accepted, a message to save to 'validated' is sent table via 'daily_save' function
    """

    template_name = "daily_validation.html"
    form_class = DailyValidationForm
    success_url = "/validated/daily_validation/"

    def post(self, request, *args, **kwargs):
        form = DailyValidationForm(self.request.POST or None)
        if form.is_valid():
            if functions.is_ajax(self.request):
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

        # return render(request, "home/form_error.html", {"form": form})


class DetailList(ListView):
    """
    Sends a table with calculation for one day only. This table is sub-hourly.
    It takes into account 'measurement' and 'validated' data
    It has quality check indicators: time delta, threshold errors, etc.
    """

    template_name = "home/message.html"

    def get(self, request, *args, **kwargs):
        if functions.is_ajax(self.request):
            station_id = kwargs.get("station_id")
            variable_id = kwargs.get("variable_id")
            date = kwargs.get("date")
            minimum = Decimal(kwargs.get("minimum"))
            maximum = Decimal(kwargs.get("maximum"))

            station = Station.objects.get(station_id=station_id)
            variable = Variable.objects.get(variable_id=variable_id)
            date = datetime.strptime(date, "%Y-%m-%d")

            data = functions.detail_list(station, variable, date, minimum, maximum)
            data_json = json.dumps(data, allow_nan=True, cls=DjangoJSONEncoder)
            return HttpResponse(data_json, content_type="application/json")
        message = "Ocurrio un problema con el procesamiento de la información, por favor contacte con el administrador"
        return render(request, "home/message.html", {"message": message})


def daily_save(request):
    """
    Recieves the signal from the user interface (Validation interface) to save data to 'validated' table.
    It also has information for the days the user wants to delete (make them NULL) in the 'validated' table
    """
    station_id = int(request.POST.get("station_id", None))
    variable_id = int(request.POST.get("variable_id", None))
    maximum = Decimal(request.POST.get("maximum", None))
    minimum = Decimal(request.POST.get("minimum", None))
    changes_json = request.POST.get("changes", None)

    station = Station.objects.get(station_id=station_id)
    variable = Variable.objects.get(variable_id=variable_id)
    changes_list = json.loads(changes_json)

    conditions = functions.get_conditions(changes_list)

    result = functions.save_to_validated(
        variable,
        station,
        conditions,
        changes_list[0]["date"],
        changes_list[-1]["date"],
        minimum,
        maximum,
    )

    return JsonResponse({"result": result})


def detail_save(request):
    """
    Receives the data from the user interface to be stored in validated.
    The request comes from "Detail of Selected Day" tab in the validation user interface
    """
    station_id = int(request.POST.get("station_id", None))
    variable_id = int(request.POST.get("variable_id", None))
    data_json = request.POST.get("data", None)

    variable = Variable.objects.get(variable_id=variable_id)
    station = Station.objects.get(station_id=station_id)
    data_list = json.loads(data_json)
    result = functions.save_detail_to_validated(data_list, variable, station)
    return JsonResponse({"result": result})


class DataReport(FormView):
    """
    Form for plotting and downloading data from differente tables: measurement, validated, hourly, daily, monthly.
    """

    template_name = "data_report.html"
    form_class = DataReportForm
    success_url = "/validated/data_report/"

    def post(self, request, *args, **kwargs):
        form = DataReportForm(self.request.POST or None)
        if form.is_valid():
            if functions.is_ajax(self.request):
                temporality = form.cleaned_data["temporality"]
                station = form.cleaned_data["station"]
                variable = form.cleaned_data["variable"]
                start_date = form.cleaned_data["start_date"]
                end_date = form.cleaned_data["end_date"]
                request_type = form.cleaned_data.get("request_type", None)
                if request_type == "json" or request_type == None:
                    dict_response = functions.dict_data_report(
                        temporality, station, variable, start_date, end_date
                    )
                    json_response = json.dumps(
                        dict_response, allow_nan=True, cls=DjangoJSONEncoder
                    )
                    return HttpResponse(json_response, content_type="application/json")
                elif request_type == "csv":
                    csv_response = functions.csv_data_report(
                        temporality, station, variable, start_date, end_date
                    )
                    response = HttpResponse(csv_response, content_type="text/csv")
                    response["Content-Disposition"] = 'attachment; filename="datos.csv"'
                    return response
        return render(request, "home/message.html", {"message": form})


class DailyValidationDash(View):
    def get(self, request, *args, **kwargs):
        return render(request, "daily_validation_dash.html")


def view_launch_report_calculations(request):
    """
    Function that receives the signal for calculating reports: hourly, daily, monthly from user interface
    """
    functions.launch_report_calculations()
    response = {"response": "Report calculations launch successfully!"}
    return JsonResponse(response)
