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

from importing import views

app_name = "importing"
urlpatterns = [
    re_path(
        r"data_import_temp/create/$",
        views.DataImportTempCreate.as_view(),
        name="data_import_temp_create",
    ),
    re_path(
        r"data_import_temp/detail/(?P<pk>[0-9]+)/$",
        views.DataImportTempDetail.as_view(),
        name="data_import_temp_detail",
    ),
    re_path(
        r"^data_import/$", views.DataImportFullList.as_view(), name="data_import_index"
    ),
    re_path(
        r"data_import/detail/(?P<pk>[0-9]+)/$",
        views.DataImportFullDetail.as_view(),
        name="data_import_detail",
    ),
    re_path(
        r"data_import/download/(?P<pk>[0-9]+)/$",
        views.DataImportDownload,
        name="data_import_download",
    ),
    re_path(r"^ajax/data_import/formats", views.list_formats, name="formats"),
]
