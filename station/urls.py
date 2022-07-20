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
    path("country/", views.CountryList.as_view()),
    path("country/<int:pk>/", views.CountryDetail.as_view()),
    path("region/", views.RegionList.as_view()),
    path("region/<int:pk>/", views.RegionDetail.as_view()),
    path("ecosystem/", views.EcosystemList.as_view()),
    path("ecosystem/<int:pk>/", views.EcosystemDetail.as_view()),
    path("institution/", views.InstitutionList.as_view()),
    path("institution/<int:pk>/", views.InstitutionDetail.as_view()),
    path("stationtype/", views.StationTypeList.as_view()),
    path("stationtype/<int:pk>/", views.StationTypeDetail.as_view()),
    path("place/", views.PlaceList.as_view()),
    path("place/<int:pk>/", views.PlaceDetail.as_view()),
    path("basin/", views.BasinList.as_view()),
    path("basin/<int:pk>/", views.BasinDetail.as_view()),
    path("placebasin/", views.PlaceBasinList.as_view()),
    path("placebasin/<int:pk>/", views.PlaceBasinDetail.as_view()),
    path("station/", views.StationList.as_view()),
    path("station/<int:pk>/", views.StationDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
