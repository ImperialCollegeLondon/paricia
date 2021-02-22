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

from django.urls import re_path, include, path
from calidad import views

app_name = 'calidad'
urlpatterns = [
    re_path(r'calidad/grafico1$', views.Grafico1View.as_view(), name='grafico1'),
    re_path(r'ajax/calidad/consulta_grafico1', views.consulta_grafico1, name='consulta_grafico1'),

    re_path(r'calidad/crudos_grafico1$', views.CrudosGrafico1View.as_view(), name='crudos_grafico1'),
    re_path(r'ajax/calidad/consulta_crudos_grafico1', views.consulta_crudos_grafico1, name='consulta_crudos_grafico1'),

    re_path(r'calidad/grafico2$', views.Grafico2View.as_view(), name='grafico2'),
    re_path(r'ajax/calidad/consulta_grafico2', views.consulta_grafico2, name='consulta_grafico2'),


    re_path(r'calidad/asociacionhidro/$', views.AsociacionHidroList.as_view(), name='asociacionhidro_index'),
    re_path(r'calidad/asociacionhidro/detail/(?P<pk>\d+)/$', views.AsociacionHidroDetail.as_view(),
            name='asociacionhidro_detail'),
    re_path(r'calidad/asociacionhidro/create/$', views.AsociacionHidroCreate.as_view(),
            name='asociacionhidro_create'),
    re_path(r'calidad/asociacionhidro/update/(?P<pk>\d+)/$', views.AsociacionHidroUpdate.as_view(),
            name='asociacionhidro_update'),
    re_path(r'calidad/asociacionhidro/delete/(?P<pk>\d+)/$', views.AsociacionHidroDelete.as_view(),
            name='asociacionhidro_delete'),

    re_path(r'calidad/comparar_hidro$', views.CompararHidroView.as_view(), name='comparar_hidro'),
    re_path(r'calidad/cargar_estaciones_hidro$', views.cargar_estaciones_hidro, name='cargar_estaciones_hidro'),
    re_path(r'ajax/calidad/consulta_comparar_hidro', views.consulta_comparar_hidro, name='consulta_comparar_hidro'),

    re_path(r'calidad/usuariovariable_perm/$', views.UsuarioVariableList.as_view(), name='usuariovariable_index'),
    re_path(r'calidad/usuariovariable_perm/detail/(?P<pk>\d+)/$', views.UsuarioVariableDetail.as_view(),
            name='usuariovariable_detail'),
    re_path(r'calidad/usuariovariable_perm/create/$', views.UsuarioVariableCreate.as_view(),
            name='usuariovariable_create'),
    re_path(r'calidad/usuariovariable_perm/update/(?P<pk>\d+)/$', views.UsuarioVariableUpdate.as_view(),
            name='usuariovariable_update'),
    re_path(r'calidad/usuariovariable_perm/delete/(?P<pk>\d+)/$', views.UsuarioVariableDelete.as_view(),
            name='usuariovariable_delete'),
]
