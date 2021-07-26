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

from django.urls import path
from .views import *

app_name = 'indices'
urlpatterns = [
    path('indices/doblemasa/', Doblemasa.as_view(), name='doblemasa'),
    path('indices/precipitacion/', IndPrecip.as_view(), name='precipitacion'),
    path('indices/caudal/', IndCaudal.as_view(), name='caudal'),
    path('indices/intensidad/', IntensidadRR.as_view(), name='intensidad'),
    path('indices/intensidadmulti/', IntensidadRRMultiestacion.as_view(), name='intensidadmulti'),
    path('indices/duracaudal/', DuracionCaudal.as_view(), name='duracaudal'),
    path('indices/export/', DuracionCaudalExport.as_view(), name='export'),
    path('indices/duracaudalmulti/', DuracionCaudalMultiestacion.as_view(), name='duracaudalmulti'),
    path('indices/rangos/', PeriodoDatos.as_view(), name='rangos'),
    #path('indices/caudal_exp',)
    path('indices/listar_anio/<int:estacion>', listar_anio, name='listar_anio'),
    path('indices/listar_anio_multi/', listar_anio_multi, name='listar_anio_multi'),
    path('indices/listar_fecha_caudal/<int:estacion>', listar_fecha_caudal, name='listar_fecha_caudal'),
    path('indices/listar_fecha_precipitacion/<int:estacion>', listar_fecha_precipitacion, name='listar_fecha_precipitacion'),
    path('indices/escorrentia/', EscorrentiaView.as_view(), name='escorrentia'),
    path('indices/estaciones_en_cuenca/<int:sitiocuenca_id>', estaciones_en_cuenca, name='estaciones_en_cuenca'),
]
