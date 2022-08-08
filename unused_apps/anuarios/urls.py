# -*- coding: utf-8 -*-

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

from django.urls import path, re_path

from anuarios import views

app_name = "anuarios"
urlpatterns = [
    # url(r'^anuarios/$',views.ValidacionList.as_view(),name='validacion_index'),
    path(
        "anuarios/procesar/",
        views.ProcesarVariables.as_view(),
        name="anuarios_procesar",
    ),
    # path('anuarios/variables/', views.lista_variables, name='anuarios_variables'),
    path(
        "anuarios/variables/<int:estacion>",
        views.lista_variables,
        name="anuarios_variables",
    ),
    path("anuarios/listar_anio/<int:estacion>/", views.listar_anio, name="listar_anio"),
]
