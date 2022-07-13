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

from sensor import views

app_name = "sensor"
urlpatterns = [
    path("sensortypes/", views.SensorTypeList.as_view()),
    path("sensortypes/<int:pk>/", views.SensorTypeDetail.as_view()),
    path("sensorbrands/", views.SensorBrandList.as_view()),
    path("sensorbrands/<int:pk>/", views.SensorBrandDetail.as_view()),
    path("sensors/", views.SensorList.as_view()),
    path("sensors/<int:pk>/", views.SensorDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
