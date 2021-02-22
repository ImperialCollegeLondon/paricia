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
from validacion_v2 import views

app_name = 'validacion_v2'
urlpatterns = [
    path('validacion_v2/periodos_validacion/', views.PeriodosValidacion.as_view(), name='v2_periodos_validacion'),
    path('validacion_v2/borrar/', views.ValidacionBorrar.as_view(), name='v2_borrar'),
    path('validacion_v2/diaria/', views.ValidacionDiaria.as_view(), name='v2_diaria'),
    path('validacion_v2/guardarcrudos/', views.guardar_crudos, name='v2_guardar_crudos'),
    path('validacion_v2/guardarvalidados/', views.guardar_validados, name='v2_guardar_validados'),
    path('validacion_v2/eliminarvalidados/', views.eliminar_validados, name='v2_eliminar_validados'),
    path('validacion_v2/lista/<int:estacion>/<int:variable>/<str:fecha>/<str:maximo>/<str:minimo>/', views.ListaValidacion.as_view(), name='v2_horario'),
    path('validacion_v2/', views.ValidacionList.as_view(), name='validacion_v2_index'),
]