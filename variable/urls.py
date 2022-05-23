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

app_name = "variable"
urlpatterns = [
    re_path(r"variable/$", views.VariableList.as_view(), name="variable_index"),
    re_path(
        r"variable/__super__create/$",
        views.VariableCreate.as_view(),
        name="variable_create",
    ),
    re_path(
        r"variable/detail/(?P<pk>[0-9]+)/$",
        views.VariableDetail.as_view(),
        name="variable_detail",
    ),
    re_path(
        r"variable/(?P<pk>[0-9]+)/$",
        views.VariableUpdate.as_view(),
        name="variable_update",
    ),
    re_path(
        r"variable/(?P<pk>[0-9]+)/__super__delete/$",
        views.VariableDelete.as_view(),
        name="variable_delete",
    ),
    re_path(r"variable/export/$", views.VariableExport, name="variable_export"),
    re_path(r"unit/$", views.unitList.as_view(), name="unit_index"),
    re_path(r"unit/create/$", views.unitCreate.as_view(), name="unit_create"),
    re_path(
        r"unit/detail/(?P<pk>[0-9]+)/$",
        views.unitDetail.as_view(),
        name="unit_detail",
    ),
    re_path(r"unit/(?P<pk>[0-9]+)/$", views.unitUpdate.as_view(), name="unit_update"),
    re_path(
        r"unit/(?P<pk>[0-9]+)/delete/$",
        views.unitDelete.as_view(),
        name="unit_delete",
    ),
    re_path(
        r"sensorinstallation/$",
        views.SensorInstallationList.as_view(),
        name="sensorinstallation_index",
    ),
    re_path(
        r"sensorinstallation/create/$",
        views.SensorInstallationCreate.as_view(),
        name="sensorinstallation_create",
    ),
    re_path(
        r"sensorinstallation/detail/(?P<pk>[0-9]+)/$",
        views.SensorInstallationDetail.as_view(),
        name="sensorinstallation_detail",
    ),
    re_path(
        r"sensorinstallation/edit/(?P<pk>[0-9]+)/$",
        views.SensorInstallationUpdate.as_view(),
        name="sensorinstallation_update",
    ),
    re_path(
        r"sensorinstallation/(?P<pk>[0-9]+)/delete/$",
        views.SensorInstallationDelete.as_view(),
        name="sensorinstallation_delete",
    ),
    path("variable/limits/", views.get_limits, name="variable_limits"),
]
