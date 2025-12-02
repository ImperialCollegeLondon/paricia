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
from .views import MeasurementDataAPIView

app_name = "measurement"
urlpatterns = [
    path("data_report/", views.DataReport.as_view(), name="data_report"),
    path("daily_validation/", views.DailyValidation.as_view(), name="daily_validation"),
    # API endpoint for downloading measurement data
    path("api/data/", MeasurementDataAPIView.as_view(), name="api_data"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
