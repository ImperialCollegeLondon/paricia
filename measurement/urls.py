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

app_name = "measurement"
urlpatterns = [
    path("polarwind/", views.PolarWindList.as_view()),
    path("dischargecurve/", views.DischargeCurveList.as_view()),
    path("levelfunction/", views.LevelFunctionList.as_view()),
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
]

urlpatterns = format_suffix_patterns(urlpatterns)
