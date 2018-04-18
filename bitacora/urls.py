from django.urls import re_path, include
from bitacora import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'bitacora'
urlpatterns = [
    re_path(r'bitacora/$', views.BitacoraList.as_view(), name='bitacora_index'),
    re_path(r'bitacora/(?P<page>[0-9]+)/$', views.BitacoraList.as_view(), name='bitacora_index'),
    re_path(r'bitacora/create/$', views.BitacoraCreate.as_view(), name='bitacora_create'),
    re_path(r'bitacora/detail/(?P<pk>[0-9]+)/$', views.BitacoraDetail.as_view(), name='bitacora_detail'),
    re_path(r'bitacora/edit/(?P<pk>[0-9]+)/$', views.BitacoraUpdate.as_view(), name='bitacora_update'),
    re_path(r'bitacora/(?P<pk>[0-9]+)/delete/$', views.BitacoraDelete.as_view(), name='bitacora_delete'),

]
