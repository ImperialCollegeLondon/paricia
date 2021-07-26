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

app_name = 'frecuencia'
urlpatterns = [
    re_path(r'frecuencia/$', views.FrecuenciaList.as_view(), name='frecuencia_index'),
    re_path(r'frecuencia/create/$', views.FrecuenciaCreate.as_view(), name='frecuencia_create'),
    re_path(r'frecuencia/edit/(?P<pk>[0-9]+)/$', views.FrecuenciaUpdate.as_view(), name='frecuencia_update'),
    re_path(r'frecuencia/(?P<pk>[0-9]+)/delete/$', views.FrecuenciaDelete.as_view(), name='frecuencia_delete'),
]
