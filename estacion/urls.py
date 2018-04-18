from django.urls import re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'estacion'
urlpatterns = [
    re_path(r'estacion/$', views.EstacionList.as_view(), name='estacion_index'),
    re_path(r'estacion/(?P<page>[0-9]+)/$', views.EstacionList.as_view(), name='estacion_index'),
    re_path(r'estacion/create/$', views.EstacionCreate.as_view(), name='estacion_create'),
    re_path(r'estacion/detail/(?P<pk>[0-9]+)/$', views.EstacionDetail.as_view(), name='estacion_detail'),
    re_path(r'estacion/edit/(?P<pk>[0-9]+)/$', views.EstacionUpdate.as_view(), name='estacion_update'),
    re_path(r'estacion/(?P<pk>[0-9]+)/delete/$', views.EstacionDelete.as_view(), name='estacion_delete'),

]
