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
from instalacion import views

app_name = 'instalacion'
urlpatterns = [
    re_path(r'instalacion/$', views.InstalacionList.as_view(), name='instalacion_index'),
    re_path(r'instalacion/create/$', views.InstalacionCreate.as_view(), name='instalacion_create'),
    re_path(r'instalacion/detail/(?P<pk>[0-9]+)/$', views.InstalacionDetail.as_view(), name='instalacion_detail'),
    re_path(r'instalacion/edit/(?P<pk>[0-9]+)/$', views.InstalacionUpdate.as_view(), name='instalacion_update'),
    re_path(r'instalacion/(?P<pk>[0-9]+)/delete/$', views.InstalacionDelete.as_view(), name='instalacion_delete'),

]
