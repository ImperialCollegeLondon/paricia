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
from sensor import views


app_name = 'sensor'
urlpatterns = [
    re_path(r'sensor/$', views.SensorList.as_view(), name='sensor_index'),
    re_path(r'sensor/create/$', views.SensorCreate.as_view(), name='sensor_create'),
    re_path(r'sensor/detail/(?P<pk>[0-9]+)/$', views.SensorDetail.as_view(), name='sensor_detail'),
    re_path(r'sensor/edit/(?P<pk>[0-9]+)/$', views.SensorUpdate.as_view(), name='sensor_update'),
    re_path(r'sensor/(?P<pk>[0-9]+)/delete/$', views.SensorDelete.as_view(), name='sensor_delete'),
    re_path(r'sensor/export/$', views.SensorExport, name='sensor_export'),
    re_path(r'^ajax/lista_sensores', views.ListaSensores, name='lista_sensores'),

    re_path(r'sensor/marca/$', views.MarcaList.as_view(), name='marca_index'),
    re_path(r'sensor/marca/create/$', views.MarcaCreate.as_view(), name='marca_create'),
    re_path(r'sensor/marca/detail/(?P<pk>[0-9]+)/$', views.MarcaDetail.as_view(), name='marca_detail'),
    re_path(r'sensor/marca/edit/(?P<pk>[0-9]+)/$', views.MarcaUpdate.as_view(), name='marca_update'),
    re_path(r'sensor/marca/(?P<pk>[0-9]+)/delete/$', views.MarcaDelete.as_view(), name='marca_delete'),

    re_path(r'sensor/tipo/$', views.TipoList.as_view(), name='tipo_index'),
    re_path(r'sensor/tipo/create/$', views.TipoCreate.as_view(), name='tipo_create'),
    re_path(r'sensor/tipo/detail/(?P<pk>[0-9]+)/$', views.TipoDetail.as_view(), name='tipo_detail'),
    re_path(r'sensor/tipo/edit/(?P<pk>[0-9]+)/$', views.TipoUpdate.as_view(), name='tipo_update'),
    re_path(r'sensor/tipo/(?P<pk>[0-9]+)/delete/$', views.TipoDelete.as_view(), name='tipo_delete'),
]
