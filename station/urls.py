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

app_name = "estacion"
urlpatterns = [
    re_path(r"^estacion/$", views.EstacionList.as_view(), name="estacion_index"),
    re_path(
        r"^estacion/create/$", views.EstacionCreate.as_view(), name="estacion_create"
    ),
    re_path(
        r"^estacion/detail/(?P<pk>[0-9]+)/$",
        views.EstacionDetail.as_view(),
        name="estacion_detail",
    ),
    re_path(
        r"^estacion/edit/(?P<pk>[0-9]+)/$",
        views.EstacionUpdate.as_view(),
        name="estacion_update",
    ),
    re_path(
        r"^estacion/(?P<pk>[0-9]+)/delete/$",
        views.EstacionDelete.as_view(),
        name="estacion_delete",
    ),
    re_path(r"^estacion/export/$", views.EstacionExport, name="estacion_export"),
    re_path(
        r"^ajax/estacion_consulta", views.estacion_consulta, name="estacion_consulta"
    ),
    # re_path(r'^ajax/estacion_listar', views.estacion_listar, name='estacion_listar'),
    ## URLS no debe contener tildes o el browser lo traduce a UNICODE
    re_path(r"^estacion/pais/$", views.PaisList.as_view(), name="pais_index"),
    re_path(r"^estacion/pais/create/$", views.PaisCreate.as_view(), name="pais_create"),
    re_path(
        r"^estacion/pais/detail/(?P<pk>[0-9]+)/$",
        views.PaisDetail.as_view(),
        name="pais_detail",
    ),
    re_path(
        r"^estacion/pais/(?P<pk>[0-9]+)/$",
        views.PaisUpdate.as_view(),
        name="pais_update",
    ),
    re_path(
        r"^estacion/pais/(?P<pk>[0-9]+)/delete/$",
        views.PaisDelete.as_view(),
        name="pais_delete",
    ),
    re_path(r"^estacion/region/$", views.RegionList.as_view(), name="region_index"),
    re_path(
        r"^estacion/region/create/$", views.RegionCreate.as_view(), name="region_create"
    ),
    re_path(
        r"^estacion/region/detail/(?P<pk>[0-9]+)/$",
        views.RegionDetail.as_view(),
        name="region_detail",
    ),
    re_path(
        r"^estacion/region/(?P<pk>[0-9]+)/$",
        views.RegionUpdate.as_view(),
        name="region_update",
    ),
    re_path(
        r"^estacion/region/(?P<pk>[0-9]+)/delete/$",
        views.RegionDelete.as_view(),
        name="region_delete",
    ),
    re_path(
        r"^estacion/ecosistema/$",
        views.EcosistemaList.as_view(),
        name="ecosistema_index",
    ),
    re_path(
        r"^estacion/ecosistema/create/$",
        views.EcosistemaCreate.as_view(),
        name="ecosistema_create",
    ),
    re_path(
        r"^estacion/ecosistema/detail/(?P<pk>[0-9]+)/$",
        views.EcosistemaDetail.as_view(),
        name="ecosistema_detail",
    ),
    re_path(
        r"^estacion/ecosistema/(?P<pk>[0-9]+)/$",
        views.EcosistemaUpdate.as_view(),
        name="ecosistema_update",
    ),
    re_path(
        r"^estacion/ecosistema/(?P<pk>[0-9]+)/delete/$",
        views.EcosistemaDelete.as_view(),
        name="ecosistema_delete",
    ),
    re_path(r"^estacion/socio/$", views.SocioList.as_view(), name="socio_index"),
    re_path(
        r"^estacion/socio/create/$", views.SocioCreate.as_view(), name="socio_create"
    ),
    re_path(
        r"^estacion/socio/detail/(?P<pk>[0-9]+)/$",
        views.SocioDetail.as_view(),
        name="socio_detail",
    ),
    re_path(
        r"^estacion/socio/(?P<pk>[0-9]+)/$",
        views.SocioUpdate.as_view(),
        name="socio_update",
    ),
    re_path(
        r"^estacion/socio/(?P<pk>[0-9]+)/delete/$",
        views.SocioDelete.as_view(),
        name="socio_delete",
    ),
    re_path(r"^estacion/tipo/$", views.TipoList.as_view(), name="tipo_index"),
    re_path(r"^estacion/tipo/create/$", views.TipoCreate.as_view(), name="tipo_create"),
    re_path(
        r"^estacion/tipo/detail/(?P<pk>[0-9]+)/$",
        views.TipoDetail.as_view(),
        name="tipo_detail",
    ),
    re_path(
        r"^estacion/tipo/(?P<pk>[0-9]+)/$",
        views.TipoUpdate.as_view(),
        name="tipo_update",
    ),
    re_path(
        r"^estacion/tipo/(?P<pk>[0-9]+)/delete/$",
        views.TipoDelete.as_view(),
        name="tipo_delete",
    ),
    re_path(r"^estacion/sitio/$", views.SitioList.as_view(), name="sitio_index"),
    re_path(
        r"^estacion/sitio/create/$", views.SitioCreate.as_view(), name="sitio_create"
    ),
    re_path(
        r"^estacion/sitio/detail/(?P<pk>[0-9]+)/$",
        views.SitioDetail.as_view(),
        name="sitio_detail",
    ),
    re_path(
        r"^estacion/sitio/(?P<pk>[0-9]+)/$",
        views.SitioUpdate.as_view(),
        name="sitio_update",
    ),
    re_path(
        r"^estacion/sitio/(?P<pk>[0-9]+)/delete/$",
        views.SitioDelete.as_view(),
        name="sitio_delete",
    ),
    re_path(r"^estacion/cuenca/$", views.CuencaList.as_view(), name="cuenca_index"),
    re_path(
        r"^estacion/cuenca/create/$", views.CuencaCreate.as_view(), name="cuenca_create"
    ),
    re_path(
        r"^estacion/cuenca/detail/(?P<pk>[0-9]+)/$",
        views.CuencaDetail.as_view(),
        name="cuenca_detail",
    ),
    re_path(
        r"^estacion/cuenca/(?P<pk>[0-9]+)/$",
        views.CuencaUpdate.as_view(),
        name="cuenca_update",
    ),
    re_path(
        r"^estacion/cuenca/(?P<pk>[0-9]+)/delete/$",
        views.CuencaDelete.as_view(),
        name="cuenca_delete",
    ),
    re_path(
        r"^estacion/cuenca/download_ficha/(?P<pk>[0-9]+)/$",
        views.cuenca_download_ficha,
        name="cuenca_download_ficha",
    ),
    re_path(
        r"^estacion/sitiocuenca/$",
        views.SitioCuencaList.as_view(),
        name="sitiocuenca_index",
    ),
    re_path(
        r"^estacion/sitiocuenca/create/$",
        views.SitioCuencaCreate.as_view(),
        name="sitiocuenca_create",
    ),
    re_path(
        r"^estacion/sitiocuenca/detail/(?P<pk>[0-9]+)/$",
        views.SitioCuencaDetail.as_view(),
        name="sitiocuenca_detail",
    ),
    re_path(
        r"^estacion/sitiocuenca/(?P<pk>[0-9]+)/$",
        views.SitioCuencaUpdate.as_view(),
        name="sitiocuenca_update",
    ),
    re_path(
        r"^estacion/sitiocuenca/(?P<pk>[0-9]+)/delete/$",
        views.SitioCuencaDelete.as_view(),
        name="sitiocuenca_delete",
    ),
    path("estacion/getjson", views.datos_json_estaciones, name="jsonestaciones"),
    path(
        "estacion/listar_anio/<int:estacion>/<int:var>/",
        views.listar_anio,
        name="listar_anio",
    ),
]
