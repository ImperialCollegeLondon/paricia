from django.urls import re_path, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'formato'
urlpatterns = [
    re_path(r'formato/$', views.FormatoList.as_view(), name='formato_index'),
    re_path(r'formato/(?P<page>[0-9]+)/$', views.FormatoList.as_view(), name='formato_index'),
    re_path(r'formato/create/$', views.FormatoCreate.as_view(), name='formato_create'),
    re_path(r'formato/detail/(?P<pk>[0-9]+)/$', views.FormatoDetail.as_view(), name='formato_detail'),
    re_path(r'formato/edit/(?P<pk>[0-9]+)/$', views.FormatoUpdate.as_view(), name='formato_update'),
    re_path(r'formato/clasificacion/(?P<pk>[0-9]+)/$', views.FormatoClasificacion.as_view(), name='formato_clasificacion'),
    re_path(r'formato/(?P<pk>[0-9]+)/delete/$', views.FormatoDelete.as_view(), name='formato_delete'),

    re_path(r'^extension/$', views.ExtensionList.as_view(), name='extension_index'),
    re_path(r'extension/create/$', views.ExtensionCreate.as_view(), name='extension_create'),
    re_path(r'extension/detail/(?P<pk>[0-9]+)/$', views.ExtensionDetail.as_view(), name='extension_detail'),
    re_path(r'extension/(?P<pk>[0-9]+)/$', views.ExtensionUpdate.as_view(), name='extension_update'),
    re_path(r'extension/(?P<pk>[0-9]+)/delete/$', views.ExtensionDelete.as_view(), name='extension_delete'),

    re_path(r'^delimitador/$', views.DelimitadorList.as_view(), name='delimitador_index'),
    re_path(r'delimitador/create/$', views.DelimitadorCreate.as_view(), name='delimitador_create'),
    re_path(r'delimitador/detail/(?P<pk>[0-9]+)/$', views.DelimitadorDetail.as_view(), name='delimitador_detail'),
    re_path(r'delimitador/(?P<pk>[0-9]+)/$', views.DelimitadorUpdate.as_view(), name='delimitador_update'),
    re_path(r'delimitador/(?P<pk>[0-9]+)/delete/$', views.DelimitadorDelete.as_view(), name='delimitador_delete'),

    re_path(r'clasificacion/$', views.ClasificacionList.as_view(), name='clasificacion_index'),
    # re_path(r'clasificacion/(?P<page>[0-9]+)/$',views.ClasificacionList.as_view(),name='clasificacion_index'),
    re_path(r'clasificacion/(?P<for_id>[0-9]+)/$', views.ClasificacionList.as_view(), name='clasificacion_index'),
    re_path(r'clasificacion/create/$', views.ClasificacionCreate.as_view(), name='clasificacion_create'),
    re_path(r'clasificacion/create/(?P<for_id>[0-9]+)/$', views.ClasificacionCreate.as_view(),
         name='clasificacion_create'),
    re_path(r'clasificacion/detail/(?P<pk>[0-9]+)/$', views.ClasificacionDetail.as_view(), name='clasificacion_detail'),
    re_path(r'clasificacion/edit/(?P<pk>[0-9]+)/$', views.ClasificacionUpdate.as_view(), name='clasificacion_update'),
    re_path(r'clasificacion/(?P<pk>[0-9]+)/delete/$', views.ClasificacionDelete.as_view(), name='clasificacion_delete'),

    path('asociacion/', views.AsociacionList.as_view(), name='asociacion_index'),
    path('asociacion/<int:page>', views.AsociacionList.as_view(), name='asociacion_index'),
    re_path(r'asociacion/create/$', views.AsociacionCreate.as_view(), name='asociacion_create'),
    re_path(r'asociacion/detail/(?P<pk>[0-9]+)/$', views.AsociacionDetail.as_view(), name='asociacion_detail'),
    re_path(r'asociacion/(?P<pk>[0-9]+)/$', views.AsociacionUpdate.as_view(), name='asociacion_update'),
    re_path(r'asociacion/(?P<pk>[0-9]+)/delete/$', views.AsociacionDelete.as_view(), name='asociacion_delete'),
]
