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

app_name = "measurement"
urlpatterns = [
    re_path(
        r"^measurement/dischargecurve/$",
        views.DischargeCurveList.as_view(),
        name="dischargecurve_index",
    ),
    re_path(
        r"^measurement/dischargecurve/create/$",
        views.DischargeCurveCreate.as_view(),
        name="dischargecurve_create",
    ),
    re_path(
        r"^measurement/dischargecurve/detail/(?P<pk>[0-9]+)/$",
        views.DischargeCurveDetail.as_view(),
        name="dischargecurve_detail",
    ),
    re_path(
        r"^measurement/dischargecurve/edit/(?P<pk>[0-9]+)/$",
        views.DischargeCurveUpdate.as_view(),
        name="dischargecurve_update",
    ),
    re_path(
        r"^measurement/dischargecurve/(?P<pk>[0-9]+)/delete/$",
        views.DischargeCurveDelete.as_view(),
        name="dischargecurve_delete",
    ),
    re_path(
        r"^measurement/dischargecurve/levelfunction/create/(?P<id>[0-9]+)/$",
        views.LevelFunctionCreate.as_view(),
        name="levelfunction_create",
    ),
    re_path(
        r"^measurement/dischargecurve/levelfunction/detail/(?P<pk>[0-9]+)/$",
        views.LevelFunctionDetail.as_view(),
        name="levelfunction_detail",
    ),
    re_path(
        r"^measurement/dischargecurve/levelfunction/edit/(?P<pk>[0-9]+)/$",
        views.LevelFunctionUpdate.as_view(),
        name="levelfunction_update",
    ),
    re_path(
        r"^measurement/dischargecurve/levelfunction/(?P<pk>[0-9]+)/delete/$",
        views.LevelFunctionDelete.as_view(),
        name="levelfunction_delete",
    ),
    re_path(
        r"^measurement/dischargecurve/recalculate_flow/$",
        views.recalculate_flow,
        name="recalculate_flow",
    ),
]
