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

app_name = "formatting"
urlpatterns = [
    re_path(r"^formatting/date/$", views.DateList.as_view(), name="date_index"),
    re_path(
        r"^formatting/date/create/$", views.DateCreate.as_view(), name="date_create"
    ),
    re_path(
        r"^formatting/date/detail/(?P<pk>[0-9]+)/$",
        views.DateDetail.as_view(),
        name="date_detail",
    ),
    re_path(
        r"^formatting/date/(?P<pk>[0-9]+)/$",
        views.DateUpdate.as_view(),
        name="date_update",
    ),
    re_path(
        r"^formatting/date/(?P<pk>[0-9]+)/delete/$",
        views.DateDelete.as_view(),
        name="date_delete",
    ),
    re_path(r"^formatting/time/$", views.TimeList.as_view(), name="time_index"),
    re_path(
        r"^formatting/time/create/$", views.TimeCreate.as_view(), name="time_create"
    ),
    re_path(
        r"^formatting/time/detail/(?P<pk>[0-9]+)/$",
        views.TimeDetail.as_view(),
        name="time_detail",
    ),
    re_path(
        r"^formatting/time/(?P<pk>[0-9]+)/$",
        views.TimeUpdate.as_view(),
        name="time_update",
    ),
    re_path(
        r"^formatting/time/(?P<pk>[0-9]+)/delete/$",
        views.TimeDelete.as_view(),
        name="time_delete",
    ),
    re_path(r"formatting/$", views.FormatList.as_view(), name="format_index"),
    re_path(r"formatting/create/$", views.FormatCreate.as_view(), name="format_create"),
    re_path(
        r"formatting/detail/(?P<pk>[0-9]+)/$",
        views.FormatDetail.as_view(),
        name="format_detail",
    ),
    re_path(
        r"formatting/edit/(?P<pk>[0-9]+)/$",
        views.FormatUpdate.as_view(),
        name="format_update",
    ),
    re_path(
        r"formatting/(?P<pk>[0-9]+)/delete/$",
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
    re_path(
        r"^association/$", views.AssociationList.as_view(), name="association_index"
    ),
    re_path(
        r"association/create/$",
        views.AssociationCreate.as_view(),
        name="association_create",
    ),
    re_path(
        r"association/detail/(?P<pk>[0-9]+)/$",
        views.AssociationDetail.as_view(),
        name="association_detail",
    ),
    re_path(
        r"association/(?P<pk>[0-9]+)/$",
        views.AssociationUpdate.as_view(),
        name="association_update",
    ),
    re_path(
        r"association/(?P<pk>[0-9]+)/delete/$",
        views.AssociationDelete.as_view(),
        name="association_delete",
    ),
]
