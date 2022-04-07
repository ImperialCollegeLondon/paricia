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

from importacion import views

app_name = "importacion"
urlpatterns = [
    re_path(
        r"importacion_temp/create/$",
        views.ImportacionTempCreate.as_view(),
        name="importacion_temp_create",
    ),
    re_path(
        r"importacion_temp/detail/(?P<pk>[0-9]+)/$",
        views.ImportacionTempDetail.as_view(),
        name="importacion_temp_detail",
    ),
    re_path(
        r"^importacion/$", views.ImportacionList.as_view(), name="importacion_index"
    ),
    re_path(
        r"importacion/detail/(?P<pk>[0-9]+)/$",
        views.ImportacionDetail.as_view(),
        name="importacion_detail",
    ),
    re_path(
        r"importacion/descarga/(?P<pk>[0-9]+)/$",
        views.ImportacionDescarga,
        name="importacion_descarga",
    ),
    re_path(r"^ajax/importacion/formatos", views.lista_formatos, name="formatos"),
]
