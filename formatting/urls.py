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

app_name = "formatting"
urlpatterns = [
    path("extension/", views.ExtensionList.as_view()),
    path("extension/<int:pk>/", views.ExtensionDetail.as_view()),
    path("delimiter/", views.DelimiterList.as_view()),
    path("delimiter/<int:pk>/", views.DelimiterDetail.as_view()),
    path("date/", views.DateList.as_view()),
    path("date/<int:pk>/", views.DateDetail.as_view()),
    path("time/", views.TimeList.as_view()),
    path("time/<int:pk>/", views.TimeDetail.as_view()),
    path("format/", views.FormatList.as_view()),
    path("format/<int:pk>/", views.FormatDetail.as_view()),
    path("classification/", views.ClassificationList.as_view()),
    path("classification/<int:pk>/", views.ClassificationDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
