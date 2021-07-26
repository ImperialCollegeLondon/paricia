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
from . import views

app_name = 'variable'
urlpatterns = [
    re_path(r'variable/$', views.VariableList.as_view(), name='variable_index'),
    re_path(r'variable/__super__create/$', views.VariableCreate.as_view(), name='variable_create'),
    re_path(r'variable/detail/(?P<pk>[0-9]+)/$', views.VariableDetail.as_view(), name='variable_detail'),
    re_path(r'variable/(?P<pk>[0-9]+)/$', views.VariableUpdate.as_view(), name='variable_update'),
    re_path(r'variable/(?P<pk>[0-9]+)/__super__delete/$', views.VariableDelete.as_view(), name='variable_delete'),
    re_path(r'variable/export/$', views.VariableExport, name='variable_export'),

    re_path(r'unidad/$', views.UnidadList.as_view(), name='unidad_index'),
    re_path(r'unidad/create/$', views.UnidadCreate.as_view(), name='unidad_create'),
    re_path(r'unidad/detail/(?P<pk>[0-9]+)/$', views.UnidadDetail.as_view(), name='unidad_detail'),
    re_path(r'unidad/(?P<pk>[0-9]+)/$', views.UnidadUpdate.as_view(), name='unidad_update'),
    re_path(r'unidad/(?P<pk>[0-9]+)/delete/$', views.UnidadDelete.as_view(), name='unidad_delete'),

    re_path(r'control/$', views.ControlList.as_view(), name='control_index'),
    re_path(r'control/create/$', views.ControlCreate.as_view(), name='control_create'),
    re_path(r'control/detail/(?P<pk>[0-9]+)/$', views.ControlDetail.as_view(), name='control_detail'),
    re_path(r'control/edit/(?P<pk>[0-9]+)/$', views.ControlUpdate.as_view(), name='control_update'),
    re_path(r'control/(?P<pk>[0-9]+)/delete/$', views.ControlDelete.as_view(), name='control_delete'),


    path('variable/limites/', views.get_limites, name='variable_limites'),


]
