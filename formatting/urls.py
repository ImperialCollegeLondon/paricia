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
    path("formatting/extensions/", views.ExtensionList.as_view()),
    path("formatting/extensions/<int:pk>/", views.ExtensionDetail.as_view()),
    path("formatting/delimiters/", views.DelimiterList.as_view()),
    path("formatting/delimiters/<int:pk>/", views.DelimiterDetail.as_view()),
    path("formatting/date/", views.DateList.as_view()),
    path("formatting/date/<int:pk>/", views.DateDetail.as_view()),
    path("formatting/time/", views.TimeList.as_view()),
    path("formatting/time/<int:pk>/", views.TimeDetail.as_view()),
    path("formatting/format/", views.FormatList.as_view()),
    path("formatting/format/<int:pk>/", views.FormatDetail.as_view()),
    path("formatting/classification/", views.ClassificationList.as_view()),
    path("formatting/classification/<int:pk>/", views.ClassificationDetail.as_view()),
    path("formatting/association/", views.AssociationList.as_view()),
    path("formatting/association/<int:pk>/", views.AssociationDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
