from django.urls import re_path, path
from importacion import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'importacion'
urlpatterns = [
    re_path(r'^importacion/$', views.ImportacionList.as_view(), name='importacion_index'),
    re_path(r'^importacion/(?P<page>[0-9]+)/$', views.ImportacionList.as_view(), name='importacion_index'),
    re_path(r'importacion/create/$', views.ImportacionCreate.as_view(), name='importacion_create'),
    re_path(r'importacion/detail/(?P<pk>[0-9]+)/$', views.ImportacionDetail.as_view(), name='importacion_detail'),
    re_path(r'importacion/guardar/(?P<imp_id>[0-9]+)/$', views.guardar_archivo, name='importacion_guardar'),
    re_path(r'importacion/(?P<pk>[0-9]+)/delete/$', views.ImportacionDelete.as_view(), name='importacion_delete'),
    re_path(r'importacion/lectura/$', views.lectura_automatica, name='lectura'),
    path('importacion/automatica', views.ListAutomatico.as_view(), name='importacion_automatica'),
    path('importacion/automatica/<int:page>', views.ListAutomatico.as_view(), name='importacion_automatica'),
    re_path(r'^ajax/formatos', views.lista_formatos, name='formatos')
]
