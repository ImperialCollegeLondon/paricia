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

from django.urls import path

from importing import views

app_name = "importing"
urlpatterns = [
    path("data_import_temp/", views.DataImportTempList.as_view()),
    path("data_import_temp/create/", views.DataImportTempCreate.as_view()),
    path("data_import_temp/<int:pk>/", views.DataImportTempDetail.as_view()),
    path("data_import_full/", views.DataImportFullList.as_view()),
    path("data_import_full/create/", views.DataImportFullCreate.as_view()),
    path("data_import_full/<int:pk>/", views.DataImportFullDetail.as_view()),
]
