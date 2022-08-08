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

app_name = "variable"
urlpatterns = [
    path("unit/", views.UnitList.as_view()),
    path("unit/<int:pk>/", views.UnitDetail.as_view()),
    path("variable/", views.VariableList.as_view()),
    path("variable/<int:pk>/", views.VariableDetail.as_view()),
    path("sensorinstallation/", views.SensorInstallationList.as_view()),
    path(
        "sensorinstallation/<int:pk>/",
        views.SensorInstallationDetail.as_view(),
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns.extend([path("variable/limits/", views.get_limits, name="variable_limits")])
