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

from django.urls import re_path

from . import views

app_name = "format"
urlpatterns = [
    re_path(r"^format/date/$", views.FechaList.as_view(), name="date_index"),
    re_path(r"^format/date/create/$", views.FechaCreate.as_view(), name="date_create"),
    re_path(
        r"^format/date/detail/(?P<pk>[0-9]+)/$",
        views.FechaDetail.as_view(),
        name="date_detail",
    ),
    re_path(
        r"^format/date/(?P<pk>[0-9]+)/$",
        views.FechaUpdate.as_view(),
        name="date_update",
    ),
    re_path(
        r"^format/date/(?P<pk>[0-9]+)/delete/$",
        views.FechaDelete.as_view(),
        name="date_delete",
    ),
    re_path(r"^format/time/$", views.HoraList.as_view(), name="time_index"),
    re_path(r"^format/time/create/$", views.HoraCreate.as_view(), name="time_create"),
    re_path(
        r"^format/time/detail/(?P<pk>[0-9]+)/$",
        views.HoraDetail.as_view(),
        name="time_detail",
    ),
    re_path(
        r"^format/time/(?P<pk>[0-9]+)/$",
        views.HoraUpdate.as_view(),
        name="time_update",
    ),
    re_path(
        r"^format/time/(?P<pk>[0-9]+)/delete/$",
        views.HoraDelete.as_view(),
        name="time_delete",
    ),
    re_path(r"format/$", views.FormatoList.as_view(), name="format_index"),
    re_path(r"format/create/$", views.FormatCreate.as_view(), name="format_create"),
    re_path(
        r"format/detail/(?P<pk>[0-9]+)/$",
        views.FormatDetail.as_view(),
        name="format_detail",
    ),
    re_path(
        r"format/edit/(?P<pk>[0-9]+)/$",
        views.FormatUpdate.as_view(),
        name="format_update",
    ),
    re_path(
        r"format/(?P<pk>[0-9]+)/delete/$",
        views.FormatDelete.as_view(),
        name="format_delete",
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
    re_path(r"^delimiter/$", views.DelimiterList.as_view(), name="delimiter_index"),
    re_path(
        r"delimiter/create/$",
        views.DelimiterCreate.as_view(),
        name="delimiter_create",
    ),
    re_path(
        r"delimiter/(?P<pk>[0-9]+)/$",
        views.DelimiterUpdate.as_view(),
        name="delimiter_update",
    ),
    re_path(
        r"delimiter/(?P<pk>[0-9]+)/delete/$",
        views.DelimiterDelete.as_view(),
        name="delimiter_delete",
    ),
    re_path(
        r"clasification/create/(?P<for_id>[0-9]+)/$",
        views.ClasificationCreate.as_view(),
        name="clasification_create",
    ),
    re_path(
        r"clasification/detail/(?P<pk>[0-9]+)/$",
        views.ClasificationDetail.as_view(),
        name="clasification_detail",
    ),
    re_path(
        r"clasification/edit/(?P<pk>[0-9]+)/$",
        views.ClasificationUpdate.as_view(),
        name="clasification_update",
    ),
    re_path(
        r"clasification/(?P<pk>[0-9]+)/delete/$",
        views.ClasificationDelete.as_view(),
        name="clasification_delete",
    ),
    re_path(r"^asociation/$", views.AssociationList.as_view(), name="asociation_index"),
    re_path(
        r"asociation/create/$",
        views.AssociationCreate.as_view(),
        name="asociation_create",
    ),
    re_path(
        r"asociation/detail/(?P<pk>[0-9]+)/$",
        views.AssociationDetail.as_view(),
        name="asociation_detail",
    ),
    re_path(
        r"asociation/(?P<pk>[0-9]+)/$",
        views.AssociationUpdate.as_view(),
        name="asociation_update",
    ),
    re_path(
        r"asociation/(?P<pk>[0-9]+)/delete/$",
        views.AssociationDelete.as_view(),
        name="asociation_delete",
    ),
]
