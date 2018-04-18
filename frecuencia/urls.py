from django.urls import re_path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'frecuencia'
urlpatterns = [
    re_path(r'frecuencia/$', views.FrecuenciaList.as_view(), name='frecuencia_index'),
    re_path(r'frecuencia/(?P<page>[0-9]+)/$', views.FrecuenciaList.as_view(), name='frecuencia_index'),
    re_path(r'frecuencia/create/$', views.FrecuenciaCreate.as_view(), name='frecuencia_create'),
    re_path(r'frecuencia/detail/(?P<pk>[0-9]+)/$', views.FrecuenciaDetail.as_view(), name='frecuencia_detail'),
    re_path(r'frecuencia/edit/(?P<pk>[0-9]+)/$', views.FrecuenciaUpdate.as_view(), name='frecuencia_update'),
    re_path(r'frecuencia/(?P<pk>[0-9]+)/delete/$', views.FrecuenciaDelete.as_view(), name='frecuencia_delete'),
]
