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
    path("measurement/polarwind/", views.PolarWindList.as_view()),
    path("measurement/dischargecurve/", views.DischargeCurveList.as_view()),
    path("measurement/levelfunction/", views.LevelFunctionList.as_view()),
    path("measurement/precipitation/", views.PrecipitationList.as_view()),
    path("measurement/airtemperature/", views.AirTemperatureList.as_view()),
    path("measurement/humidity/", views.HumidityList.as_view()),
    path("measurement/windvelocity/", views.WindVelocityList.as_view()),
    path("measurement/winddirection/", views.WindDirectionList.as_view()),
    path("measurement/soilmoisture/", views.SoilMoistureList.as_view()),
    path("measurement/solarradiation/", views.SolarRadiationList.as_view()),
    path("measurement/atmosphericpressure/", views.AtmosphericPressureList.as_view()),
    path("measurement/watertemperature/", views.WaterTemperatureList.as_view()),
    path("measurement/flow/", views.FlowList.as_view()),
    path("measurement/waterlevel/", views.WaterLevelList.as_view()),
    path("measurement/batteryvoltage/", views.BatteryVoltageList.as_view()),
    path("measurement/flowmanual/", views.FlowManualList.as_view()),
    path("measurement/striplevelreading/", views.StripLevelReadingList.as_view()),
    path("measurement/soiltemperature/", views.SoilTemperatureList.as_view()),
    path("measurement/indirectradiation/", views.IndirectRadiationList.as_view()),
    path(
        "measurement/watertemperature_depth/", views.WaterTemperatureDepthList.as_view()
    ),
    path("measurement/wateracidity_depth/", views.WaterAcidityDepthList.as_view()),
    path("measurement/redoxpotential_depth/", views.RedoxPotentialDepthList.as_view()),
    path("measurement/waterturbidity_depth/", views.WaterTurbidityDepthList.as_view()),
    path(
        "measurement/chlorineconcentration_depth/",
        views.ChlorineConcentrationDepthList.as_view(),
    ),
    path(
        "measurement/oxygenconcentration_depth/",
        views.OxygenConcentrationDepthList.as_view(),
    ),
    path(
        "measurement/percentageoxygen_depth/",
        views.PercentageOxygenConcentrationDepthList.as_view(),
    ),
    path("measurement/phycocyanin_depth/", views.PhycocyaninDepthList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
