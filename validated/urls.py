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

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from .dash_apps.finished_apps import daily_validation

app_name = "validated"
urlpatterns = [
    # TODO Verify if it's not really needed
    # path("polarwind/", views.PolarWindList.as_view()),
    path("precipitation/", views.PrecipitationList.as_view()),
    path("airtemperature/", views.AirTemperatureList.as_view()),
    path("humidity/", views.HumidityList.as_view()),
    path("windvelocity/", views.WindVelocityList.as_view()),
    path("winddirection/", views.WindDirectionList.as_view()),
    path("soilmoisture/", views.SoilMoistureList.as_view()),
    path("solarradiation/", views.SolarRadiationList.as_view()),
    path("atmosphericpressure/", views.AtmosphericPressureList.as_view()),
    path("watertemperature/", views.WaterTemperatureList.as_view()),
    path("flow/", views.FlowList.as_view()),
    path("waterlevel/", views.WaterLevelList.as_view()),
    path("batteryvoltage/", views.BatteryVoltageList.as_view()),
    path("flowmanual/", views.FlowManualList.as_view()),
    path("striplevelreading/", views.StripLevelReadingList.as_view()),
    path("soiltemperature/", views.SoilTemperatureList.as_view()),
    path("indirectradiation/", views.IndirectRadiationList.as_view()),
    path("watertemperature_depth/", views.WaterTemperatureDepthList.as_view()),
    path("wateracidity_depth/", views.WaterAcidityDepthList.as_view()),
    path("redoxpotential_depth/", views.RedoxPotentialDepthList.as_view()),
    path("waterturbidity_depth/", views.WaterTurbidityDepthList.as_view()),
    path(
        "chlorineconcentration_depth/",
        views.ChlorineConcentrationDepthList.as_view(),
    ),
    path(
        "oxygenconcentration_depth/",
        views.OxygenConcentrationDepthList.as_view(),
    ),
    path(
        "percentageoxygen_depth/",
        views.PercentageOxygenConcentrationDepthList.as_view(),
    ),
    path("phycocyanin_depth/", views.PhycocyaninDepthList.as_view()),
    path("daily_validation/", views.DailyValidation.as_view(), name="daily_validation"),
    path("daily_save/", views.daily_save, name="daily_save"),
    path(
        "detail_list/<int:station_id>/<int:variable_id>/<str:date>/<str:minimum>/<str:maximum>/",
        views.DetailList.as_view(),
        name="detail_list",
    ),
    path("detail_save/", views.detail_save, name="detail_save"),
    path("data_report/", views.DataReport.as_view(), name="data_report"),
    path(
        "launch_report_calculations/",
        views.view_launch_report_calculations,
        name="launch_report_calculations",
    ),
    path(
        "daily_validation_dev/",
        views.DailyValidationDev.as_view(),
        name="daily_validation_dev",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
