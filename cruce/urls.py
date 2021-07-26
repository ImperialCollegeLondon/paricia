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
from cruce import views

app_name = 'cruce'
urlpatterns = [
    re_path(r'cruce/$', views.CruceList.as_view(), name='cruce_index'),
    re_path(r'cruce/create/$', views.CruceCreate.as_view(), name='cruce_create'),
    re_path(r'cruce/detail/(?P<pk>[0-9]+)/$', views.CruceDetail.as_view(), name='cruce_detail'),
    re_path(r'cruce/edit/(?P<pk>[0-9]+)/$', views.CruceUpdate.as_view(), name='cruce_update'),
    re_path(r'cruce/(?P<pk>[0-9]+)/delete/$', views.CruceDelete.as_view(), name='cruce_delete'),

]
