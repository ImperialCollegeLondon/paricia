from django.urls import re_path, path
from reportes import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'reportes'
urlpatterns = [
    re_path(r'^reportes/anuario/$', views.ReportesAnuario.as_view(), name='anuario'),
    re_path(r'^reportes/consultas/$', views.ConsultasPeriodo.as_view(), name='consultas_periodo'),
    re_path(r'^reportes/comparacion/$', views.ComparacionValores.as_view(), name='comparacion_reporte'),
    re_path(r'^reportes/compararvariable/$', views.ComparacionVariables.as_view(), name='comparacion_variable'),
    re_path(r'^reportes/estacionvariable/$', views.ConsultasEstacionVariable.as_view(), name='estacion_variable'),
    re_path(
        r'reportes/datos_horarios/(?P<est_id>[0-9]+)/(?P<var_id>[0-9]+)/(?P<fec_ini>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})/(?P<fec_fin>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})/$',
        views.datos_json_horarios, name='horarios'),
    path('reportes/inamhi', views.ConsultaInamhi.as_view(), name='reporte_inamhi'),
    path('parametros/inamhi', views.variables_inamhi, name='parametros_inamhi'),
]
