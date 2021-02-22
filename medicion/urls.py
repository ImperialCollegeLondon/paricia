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

app_name = 'medicion'
urlpatterns = [
    re_path(r'medicion/curvadescarga/$', views.CurvaDescargaList.as_view(), name='curvadescarga_index'),
    re_path(r'medicion/curvadescarga/create/$', views.CurvaDescargaCreate.as_view(), name='curvadescarga_create'),
    re_path(r'medicion/curvadescarga/detail/(?P<pk>[0-9]+)/$', views.CurvaDescargaDetail.as_view(), name='curvadescarga_detail'),
    re_path(r'medicion/curvadescarga/edit/(?P<pk>[0-9]+)/$', views.CurvaDescargaUpdate.as_view(), name='curvadescarga_update'),
    re_path(r'medicion/curvadescarga/(?P<pk>[0-9]+)/delete/$', views.CurvaDescargaDelete.as_view(), name='curvadescarga_delete'),

    re_path(r'^ajax/medicion_variables', views.variables, name='variables'),
]
