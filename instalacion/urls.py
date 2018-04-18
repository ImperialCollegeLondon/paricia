from django.urls import re_path
from instalacion import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'instalacion'
urlpatterns = [
    re_path(r'instalacion/$', views.InstalacionList.as_view(), name='instalacion_index'),
    re_path(r'instalacion/(?P<page>[0-9]+)/$', views.InstalacionList.as_view(), name='instalacion_index'),
    re_path(r'instalacion/create/$', views.InstalacionCreate.as_view(), name='instalacion_create'),
    re_path(r'instalacion/detail/(?P<pk>[0-9]+)/$', views.InstalacionDetail.as_view(), name='instalacion_detail'),
    re_path(r'instalacion/edit/(?P<pk>[0-9]+)/$', views.InstalacionUpdate.as_view(), name='instalacion_update'),
    re_path(r'instalacion/(?P<pk>[0-9]+)/delete/$', views.InstalacionDelete.as_view(), name='instalacion_delete'),

]
