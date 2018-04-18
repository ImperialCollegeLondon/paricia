from django.urls import re_path
from sensor import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'sensor'
urlpatterns = [
    re_path(r'sensor/$', views.SensorList.as_view(), name='sensor_index'),
    re_path(r'sensor/(?P<page>[0-9]+)/$', views.SensorList.as_view(), name='sensor_index'),
    re_path(r'sensor/create/$', views.SensorCreate.as_view(), name='sensor_create'),
    re_path(r'sensor/detail/(?P<pk>[0-9]+)/$', views.SensorDetail.as_view(), name='sensor_detail'),
    re_path(r'sensor/edit/(?P<pk>[0-9]+)/$', views.SensorUpdate.as_view(), name='sensor_update'),
    re_path(r'sensor/(?P<pk>[0-9]+)/delete/$', views.SensorDelete.as_view(), name='sensor_delete'),
]
