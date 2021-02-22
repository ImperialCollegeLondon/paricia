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
from datalogger import views

app_name = 'datalogger'
urlpatterns = [
    re_path(r'datalogger/$', views.DataloggerList.as_view(), name='datalogger_index'),
    re_path(r'datalogger/create/$', views.DataloggerCreate.as_view(), name='datalogger_create'),
    re_path(r'datalogger/detail/(?P<pk>[0-9]+)/$', views.DataloggerDetail.as_view(), name='datalogger_detail'),
    re_path(r'datalogger/edit/(?P<pk>[0-9]+)/$', views.DataloggerUpdate.as_view(), name='datalogger_update'),
    re_path(r'datalogger/(?P<pk>[0-9]+)/delete/$', views.DataloggerDelete.as_view(), name='datalogger_delete'),
    re_path(r'datalogger/export/$', views.DataloggerExport, name='datalogger_export'),
    # re_path(r'^ajax/lista_dataloggers', views.ListaDataloggers, name='lista_dataloggers'),

    re_path(r'datalogger/marca/$', views.MarcaList.as_view(), name='marca_index'),
    re_path(r'datalogger/marca/create/$', views.MarcaCreate.as_view(), name='marca_create'),
    re_path(r'datalogger/marca/detail/(?P<pk>[0-9]+)/$', views.MarcaDetail.as_view(), name='marca_detail'),
    re_path(r'datalogger/marca/edit/(?P<pk>[0-9]+)/$', views.MarcaUpdate.as_view(), name='marca_update'),
    re_path(r'datalogger/marca/(?P<pk>[0-9]+)/delete/$', views.MarcaDelete.as_view(), name='marca_delete'),
]
