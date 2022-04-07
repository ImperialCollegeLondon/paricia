################################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos (iMHEA)
# basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#         Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS), Ecuador.
#         Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones creadoras,
#              ya sea en uso total o parcial del código.

from django.urls import re_path

from . import views

app_name = "formato"
urlpatterns = [
    re_path(r"^formato/fecha/$", views.FechaList.as_view(), name="fecha_index"),
    re_path(
        r"^formato/fecha/create/$", views.FechaCreate.as_view(), name="fecha_create"
    ),
    re_path(
        r"^formato/fecha/detail/(?P<pk>[0-9]+)/$",
        views.FechaDetail.as_view(),
        name="fecha_detail",
    ),
    re_path(
        r"^formato/fecha/(?P<pk>[0-9]+)/$",
        views.FechaUpdate.as_view(),
        name="fecha_update",
    ),
    re_path(
        r"^formato/fecha/(?P<pk>[0-9]+)/delete/$",
        views.FechaDelete.as_view(),
        name="fecha_delete",
    ),
    re_path(r"^formato/hora/$", views.HoraList.as_view(), name="hora_index"),
    re_path(r"^formato/hora/create/$", views.HoraCreate.as_view(), name="hora_create"),
    re_path(
        r"^formato/hors/detail/(?P<pk>[0-9]+)/$",
        views.HoraDetail.as_view(),
        name="hora_detail",
    ),
    re_path(
        r"^formato/hora/(?P<pk>[0-9]+)/$",
        views.HoraUpdate.as_view(),
        name="hora_update",
    ),
    re_path(
        r"^formato/hora/(?P<pk>[0-9]+)/delete/$",
        views.HoraDelete.as_view(),
        name="hora_delete",
    ),
    re_path(r"formato/$", views.FormatoList.as_view(), name="formato_index"),
    re_path(r"formato/create/$", views.FormatoCreate.as_view(), name="formato_create"),
    re_path(
        r"formato/detail/(?P<pk>[0-9]+)/$",
        views.FormatoDetail.as_view(),
        name="formato_detail",
    ),
    re_path(
        r"formato/edit/(?P<pk>[0-9]+)/$",
        views.FormatoUpdate.as_view(),
        name="formato_update",
    ),
    re_path(
        r"formato/(?P<pk>[0-9]+)/delete/$",
        views.FormatoDelete.as_view(),
        name="formato_delete",
    ),
    re_path(r"^extension/$", views.ExtensionList.as_view(), name="extension_index"),
    re_path(
        r"extension/create/$", views.ExtensionCreate.as_view(), name="extension_create"
    ),
    re_path(
        r"extension/(?P<pk>[0-9]+)/$",
        views.ExtensionUpdate.as_view(),
        name="extension_update",
    ),
    re_path(
        r"extension/(?P<pk>[0-9]+)/delete/$",
        views.ExtensionDelete.as_view(),
        name="extension_delete",
    ),
    re_path(
        r"^delimitador/$", views.DelimitadorList.as_view(), name="delimitador_index"
    ),
    re_path(
        r"delimitador/create/$",
        views.DelimitadorCreate.as_view(),
        name="delimitador_create",
    ),
    re_path(
        r"delimitador/(?P<pk>[0-9]+)/$",
        views.DelimitadorUpdate.as_view(),
        name="delimitador_update",
    ),
    re_path(
        r"delimitador/(?P<pk>[0-9]+)/delete/$",
        views.DelimitadorDelete.as_view(),
        name="delimitador_delete",
    ),
    re_path(
        r"clasificacion/create/(?P<for_id>[0-9]+)/$",
        views.ClasificacionCreate.as_view(),
        name="clasificacion_create",
    ),
    re_path(
        r"clasificacion/detail/(?P<pk>[0-9]+)/$",
        views.ClasificacionDetail.as_view(),
        name="clasificacion_detail",
    ),
    re_path(
        r"clasificacion/edit/(?P<pk>[0-9]+)/$",
        views.ClasificacionUpdate.as_view(),
        name="clasificacion_update",
    ),
    re_path(
        r"clasificacion/(?P<pk>[0-9]+)/delete/$",
        views.ClasificacionDelete.as_view(),
        name="clasificacion_delete",
    ),
    re_path(r"^asociacion/$", views.AsociacionList.as_view(), name="asociacion_index"),
    re_path(
        r"asociacion/create/$",
        views.AsociacionCreate.as_view(),
        name="asociacion_create",
    ),
    re_path(
        r"asociacion/detail/(?P<pk>[0-9]+)/$",
        views.AsociacionDetail.as_view(),
        name="asociacion_detail",
    ),
    re_path(
        r"asociacion/(?P<pk>[0-9]+)/$",
        views.AsociacionUpdate.as_view(),
        name="asociacion_update",
    ),
    re_path(
        r"asociacion/(?P<pk>[0-9]+)/delete/$",
        views.AsociacionDelete.as_view(),
        name="asociacion_delete",
    ),
]
