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
from telemetria import views

app_name = 'telemetria'
urlpatterns = [

    re_path(r'telemetria/visualizar/$', views.ConsultaForm.as_view(), name='visualizar'),
    re_path(r'^ajax/telemetria/consulta/', views.Consulta, name='consulta'),
    re_path(r'telemetria/calidad/visualizar/$', views.ConsultaCalidadForm.as_view(), name='calidad_visualizar'),
    re_path(r'^ajax/telemetria/calidad/consulta/', views.ConsultaCalidad, name='calidad_consulta'),

    re_path(r'telemetria/precipitacion/$', views.PrecipitacionView.as_view(), name='precipitacion'),
    re_path(r'^ajax/telemetria/precipitacion/consulta', views.consulta_precipitacion, name='consulta_precipitacion'),

    re_path(r'telemetria/multiestacion_precipitacion/$', views.PrecipitacionMultiestacionView.as_view(),
            name='multiestacion_precipitacion'),

    re_path(r'telemetria/visualizar/config/$', views.ConfigVisualizarList.as_view(), name='configvisualizar_list'),
    re_path(r'telemetria/visualizar/config/detail/(?P<pk>\d+)/$', views.ConfigVisualizarDetail.as_view(), name='configvisualizar_detail'),
    re_path(r'telemetria/visualizar/config/create/$', views.ConfigVisualizarCreate.as_view(), name='configvisualizar_create'),
    re_path(r'telemetria/visualizar/config/update/(?P<pk>\d+)/$', views.ConfigVisualizarUpdate.as_view(), name='configvisualizar_update'),
    re_path(r'telemetria/visualizar/config/delete/(?P<pk>\d+)/$', views.ConfigVisualizarDelete.as_view(), name='configvisualizar_delete'),

    re_path(r'telemetria/calidad/visualizar/config/$', views.ConfigCalidadList.as_view(), name='configcalidad_list'),
    re_path(r'telemetria/calidad/visualizar/config/detail/(?P<pk>\d+)/$', views.ConfigCalidadDetail.as_view(),
            name='configcalidad_detail'),
    re_path(r'telemetria/calidad/visualizar/config/create/$', views.ConfigCalidadCreate.as_view(),
            name='configcalidad_create'),
    re_path(r'telemetria/calidad/visualizar/config/update/(?P<pk>\d+)/$', views.ConfigCalidadUpdate.as_view(),
            name='configcalidad_update'),
    re_path(r'telemetria/calidad/visualizar/config/delete/(?P<pk>\d+)/$', views.ConfigCalidadDelete.as_view(),
            name='configcalidad_delete'),

    re_path(r'telemetria/alarma_transmision/config/$', views.ConfigAlarmaList.as_view(),
            name='config_alarma_list'),
    re_path(r'telemetria/alarma_transmision_limites/$', views.ConfigAlarmaTransmisionLimites.as_view(),
            name='config_alarma_transmision_limites'),
    re_path(r'telemetria/alarma_email/config/create/$', views.ConfigAlarmaEmailCreate.as_view(),
            name='config_alarma_email_create'),
    re_path(r'telemetria/alarma_email/config/delete/(?P<pk>\d+)/$', views.ConfigAlarmaEmailDelete.as_view(),
            name='config_alarma_email_delete'),

    re_path(r'telemetria/mapa/alarma_transmision$', views.MapaTransmision.as_view(), name='mapa_alarma_transmision'),
    re_path(r'^ajax/telemetria/mapa_alarma_transmision', views.MapaTransmisionConsulta, name='consulta_mapa_alarma_transmision'),
]
