from django.urls import re_path
from validacion import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'validacion'
urlpatterns = [
    re_path(r'^validacion/$', views.ValidacionList.as_view(), name='validacion_index'),
    re_path(r'validacion/create/$', views.ValidacionCreate.as_view(), name='validacion_create'),
    re_path(r'validacion/detail/(?P<pk>[0-9]+)/$', views.ValidacionDetail.as_view(), name='validacion_detail'),
    re_path(r'validacion/edit/(?P<pk>[0-9]+)/$', views.ValidacionUpdate.as_view(), name='validacion_update'),
    re_path(r'validacion/(?P<pk>[0-9]+)/delete/$', views.ValidacionDelete.as_view(), name='validacion_delete'),
    re_path(r'validacion/procesar/$', views.ProcesarValidacion.as_view(), name='procesar_validacion'),

]
