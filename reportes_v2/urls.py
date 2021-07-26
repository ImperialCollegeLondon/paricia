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

from django.urls import re_path, path
from reportes_v2 import views

app_name = 'reportes_v2'
urlpatterns = [
    re_path(r'^reportes_v2/anuario/$', views.reportes_v2Anuario.as_view(), name='anuario'),
    re_path(r'^reportes_v2/consultas/$', views.ConsultasPeriodo.as_view(), name='consultas_periodo'),
    re_path(r'^reportes_v2/comparacion/$', views.ComparacionValores.as_view(), name='comparacion_reporte'),
    path('reportes_v2/comparar/estaciones', views.CompararEstacionesPublico.as_view(),
         name='comparar_estaciones_publico'),
    re_path(r'^reportes_v2/compararvariable/$', views.ComparacionVariables.as_view(), name='comparacion_variable'),
    path('reportes_v2/comparar/variable', views.ComparacionVariablesPublico.as_view(),
         name='comparacion_variable_publico'),
    re_path(r'^reportes_v2/estacionvariable/$', views.ConsultasEstacionVariable.as_view(), name='estacion_variable'),
    re_path(
        r'reportes_v2/datos_horarios/(?P<est_id>[0-9]+)/(?P<var_id>[0-9]+)/(?P<fec_ini>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})/(?P<fec_fin>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})/$',
        views.datos_json_horarios, name='horarios'),
    #path('reportes_v2/inamhi', views.ConsultaInamhi.as_view(), name='reporte_inamhi'),
    # path('parametros/inamhi', views.variables_inamhi, name='parametros_inamhi'),
    path('estaciones/tipo', views.tipo_estaciones, name='tipo_estaciones'),

    path('reportes_v2/mapa', views.ConsultaDatos.as_view(), name='mapa_estaciones'),
    path('reportes_v2/usuarios/', views.ConsultasUsuario.as_view(), name='consultas_usuario'),


    path('reportes_v2/sitio/', views.ConsultasSitio.as_view(), name='consultas_sitio'),
    # TODO mejorar url
    path('ajax/reportes_v2_estaciones/', views.estaciones, name='estaciones'),
    path('ajax/reportes_v2_cuencas/', views.cuencas, name='cuencas'),

    # Mapa de Estaciones por variable
    path('reportes_v2/mapa/variable/<int:var_id>', views.MapaCompararEstaciones.as_view(), name='mapa_estaciones_variable'),
    path('reportes_v2/mapa/variable/publico/<int:var_id>', views.MapaCompararEstacionesPublico.as_view(), name='mapa_estaciones_variable')

]
