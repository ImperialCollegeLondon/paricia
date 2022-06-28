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

from django.urls import path, re_path

from . import views

app_name = "station"
urlpatterns = [
    path("countries/", views.CountryList.as_view()),
    re_path(r"^station/$", views.StationList.as_view(), name="station_index"),
    re_path(r"^station/create/$", views.StationCreate.as_view(), name="station_create"),
    re_path(
        r"^station/detail/(?P<pk>[0-9]+)/$",
        views.StationDetail.as_view(),
        name="station_detail",
    ),
    re_path(
        r"^station/edit/(?P<pk>[0-9]+)/$",
        views.StationUpdate.as_view(),
        name="station_update",
    ),
    re_path(
        r"^station/(?P<pk>[0-9]+)/delete/$",
        views.StationDelete.as_view(),
        name="station_delete",
    ),
    re_path(r"^station/export/$", views.StationExport, name="station_export"),
    re_path(r"^ajax/station_query", views.station_query, name="station_query"),
    re_path(r"^station/country/$", views.CountryList.as_view(), name="country_index"),
    re_path(r"^station/region/$", views.RegionList.as_view(), name="region_index"),
    re_path(
        r"^station/region/create/$", views.RegionCreate.as_view(), name="region_create"
    ),
    re_path(
        r"^station/region/detail/(?P<pk>[0-9]+)/$",
        views.RegionDetail.as_view(),
        name="region_detail",
    ),
    re_path(
        r"^station/region/(?P<pk>[0-9]+)/$",
        views.RegionUpdate.as_view(),
        name="region_update",
    ),
    re_path(
        r"^station/region/(?P<pk>[0-9]+)/delete/$",
        views.RegionDelete.as_view(),
        name="region_delete",
    ),
    re_path(
        r"^station/ecosystem/$",
        views.EcosystemList.as_view(),
        name="ecosystem_index",
    ),
    re_path(
        r"^station/ecosystem/create/$",
        views.EcosystemCreate.as_view(),
        name="ecosystem_create",
    ),
    re_path(
        r"^station/ecosystem/detail/(?P<pk>[0-9]+)/$",
        views.EcosystemDetail.as_view(),
        name="ecosystem_detail",
    ),
    re_path(
        r"^station/ecosystem/(?P<pk>[0-9]+)/$",
        views.EcosystemUpdate.as_view(),
        name="ecosystem_update",
    ),
    re_path(
        r"^station/ecosystem/(?P<pk>[0-9]+)/delete/$",
        views.EcosystemDelete.as_view(),
        name="ecosystem_delete",
    ),
    re_path(
        r"^station/institution/$",
        views.InstitutionList.as_view(),
        name="institution_index",
    ),
    re_path(
        r"^station/institution/create/$",
        views.InstitutionCreate.as_view(),
        name="institution_create",
    ),
    re_path(
        r"^station/institution/detail/(?P<pk>[0-9]+)/$",
        views.InstitutionDetail.as_view(),
        name="institution_detail",
    ),
    re_path(
        r"^station/institution/(?P<pk>[0-9]+)/$",
        views.InstitutionUpdate.as_view(),
        name="institution_update",
    ),
    re_path(
        r"^station/institution/(?P<pk>[0-9]+)/delete/$",
        views.InstitutionDelete.as_view(),
        name="institution_delete",
    ),
    re_path(
        r"^station/sensor_type/$",
        views.StationTypeList.as_view(),
        name="sensor_type_index",
    ),
    re_path(
        r"^station/sensor_type/create/$",
        views.StationTypeCreate.as_view(),
        name="sensor_type_create",
    ),
    re_path(
        r"^station/sensor_type/detail/(?P<pk>[0-9]+)/$",
        views.StationTypeDetail.as_view(),
        name="sensor_type_detail",
    ),
    re_path(
        r"^station/sensor_type/(?P<pk>[0-9]+)/$",
        views.StationTypeUpdate.as_view(),
        name="sensor_type_update",
    ),
    re_path(
        r"^station/sensor_type/(?P<pk>[0-9]+)/delete/$",
        views.StationTypeDelete.as_view(),
        name="sensor_type_delete",
    ),
    re_path(r"^station/place/$", views.PlaceList.as_view(), name="place_index"),
    re_path(
        r"^station/place/create/$", views.PlaceCreate.as_view(), name="place_create"
    ),
    re_path(
        r"^station/place/detail/(?P<pk>[0-9]+)/$",
        views.PlaceDetail.as_view(),
        name="place_detail",
    ),
    re_path(
        r"^station/place/(?P<pk>[0-9]+)/$",
        views.PlaceUpdate.as_view(),
        name="place_update",
    ),
    re_path(
        r"^station/place/(?P<pk>[0-9]+)/delete/$",
        views.PlaceDelete.as_view(),
        name="place_delete",
    ),
    re_path(r"^station/basin/$", views.BasinList.as_view(), name="basin_index"),
    re_path(
        r"^station/basin/create/$", views.BasinCreate.as_view(), name="basin_create"
    ),
    re_path(
        r"^station/basin/detail/(?P<pk>[0-9]+)/$",
        views.BasinDetail.as_view(),
        name="basin_detail",
    ),
    re_path(
        r"^station/basin/(?P<pk>[0-9]+)/$",
        views.BasinUpdate.as_view(),
        name="basin_update",
    ),
    re_path(
        r"^station/basin/(?P<pk>[0-9]+)/delete/$",
        views.BasinDelete.as_view(),
        name="basin_delete",
    ),
    re_path(
        r"^station/placebasin/$",
        views.PlaceBasinList.as_view(),
        name="placebasin_index",
    ),
    re_path(
        r"^station/placebasin/create/$",
        views.PlaceBasinCreate.as_view(),
        name="placebasin_create",
    ),
    re_path(
        r"^station/placebasin/detail/(?P<pk>[0-9]+)/$",
        views.PlaceBasinDetail.as_view(),
        name="placebasin_detail",
    ),
    re_path(
        r"^station/placebasin/(?P<pk>[0-9]+)/$",
        views.PlaceBasinUpdate.as_view(),
        name="placebasin_update",
    ),
    re_path(
        r"^station/placebasin/(?P<pk>[0-9]+)/delete/$",
        views.PlaceBasinDelete.as_view(),
        name="placebasin_delete",
    ),
    path(
        "station/list_year/<int:station>/<int:var>/",
        views.list_year,
        name="list_year",
    ),
]
