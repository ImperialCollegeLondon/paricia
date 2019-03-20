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
    re_path(r'importacion/(?P<pk>[0-9]+)/delete/$', views.ImportacionDelete.as_view(), name='importacion_delete'),
    path('importacion/automatica', views.ListAutomatico.as_view(), name='importacion_automatica'),
    path('importacion/automatica/<int:page>', views.ListAutomatico.as_view(), name='importacion_automatica'),
    path('importacion/confirm/<int:pk>', views.ImportacionConfirm.as_view(), name='importacion_confirm'),
    re_path(r'^ajax/formatos', views.lista_formatos, name='formatos')
]
