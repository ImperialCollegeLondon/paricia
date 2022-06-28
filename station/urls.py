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

app_name = "station"
urlpatterns = [
    path("countries/", views.CountryList.as_view()),
    path("countries/<int:pk>/", views.CountryDetail.as_view()),
    path("regions/", views.RegionList.as_view()),
    path("regions/<int:pk>/", views.RegionDetail.as_view()),
    path("ecosystems/", views.EcosystemList.as_view()),
    path("ecosystems/<int:pk>/", views.EcosystemDetail.as_view()),
    path("institutions/", views.InstitutionList.as_view()),
    path("institutions/<int:pk>/", views.InstitutionDetail.as_view()),
    path("stationtypes/", views.StationTypeList.as_view()),
    path("stationtypes/<int:pk>/", views.StationTypeDetail.as_view()),
    path("places/", views.PlaceList.as_view()),
    path("places/<int:pk>/", views.PlaceDetail.as_view()),
    path("basins/", views.BasinList.as_view()),
    path("basins/<int:pk>/", views.BasinDetail.as_view()),
    path("placebasins/", views.PlaceBasinList.as_view()),
    path("placebasins/<int:pk>/", views.PlaceBasinDetail.as_view()),
    path("stations/", views.StationList.as_view()),
    path("stations/<int:pk>/", views.StationDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
