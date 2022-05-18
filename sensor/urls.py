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

from sensor import views

app_name = "sensor"
urlpatterns = [
    re_path(r"sensor/$", views.SensorList.as_view(), name="sensor_index"),
    re_path(r"sensor/create/$", views.SensorCreate.as_view(), name="sensor_create"),
    re_path(
        r"sensor/detail/(?P<pk>[0-9]+)/$",
        views.SensorDetail.as_view(),
        name="sensor_detail",
    ),
    re_path(
        r"sensor/edit/(?P<pk>[0-9]+)/$",
        views.SensorUpdate.as_view(),
        name="sensor_update",
    ),
    re_path(
        r"sensor/(?P<pk>[0-9]+)/delete/$",
        views.SensorDelete.as_view(),
        name="sensor_delete",
    ),
    re_path(r"sensor/export/$", views.SensorExport, name="sensor_export"),
    re_path(r"^ajax/lista_sensores", views.ListaSensores, name="list_sensors"),
    re_path(r"sensor/brand/$", views.SensorBrandList.as_view(), name="brand_index"),
    re_path(
        r"sensor/brand/create/$", views.SensorBrandCreate.as_view(), name="brand_create"
    ),
    re_path(
        r"sensor/brand/detail/(?P<pk>[0-9]+)/$",
        views.SensorBrandDetail.as_view(),
        name="brand_detail",
    ),
    re_path(
        r"sensor/brand/edit/(?P<pk>[0-9]+)/$",
        views.SensorBrandUpdate.as_view(),
        name="brand_update",
    ),
    re_path(
        r"sensor/brand/(?P<pk>[0-9]+)/delete/$",
        views.SensorBrandDelete.as_view(),
        name="brand_delete",
    ),
    re_path(r"sensor/type/$", views.SensorTypeList.as_view(), name="type_index"),
    re_path(
        r"sensor/type/create/$", views.SensorTypeCreate.as_view(), name="type_create"
    ),
    re_path(
        r"sensor/type/detail/(?P<pk>[0-9]+)/$",
        views.SensorTypeDetail.as_view(),
        name="type_detail",
    ),
    re_path(
        r"sensor/type/edit/(?P<pk>[0-9]+)/$",
        views.SensorTypeUpdate.as_view(),
        name="type_update",
    ),
    re_path(
        r"sensor/type/(?P<pk>[0-9]+)/delete/$",
        views.SensorTypeDelete.as_view(),
        name="type_delete",
    ),
]
