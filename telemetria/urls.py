from django.urls import re_path, path
from telemetria import views

app_name = 'telemetria'
urlpatterns = [
    re_path(r'telemetria/visualizar/$', views.ConsultaForm.as_view(), name='visualizar'),

    re_path(r'^ajax/telemetria/consulta', views.Consulta, name='consulta'),

    re_path(r'telemetria/precipitacion/$', views.PrecipitacionView.as_view(), name='precipitacion'),
    re_path(r'^ajax/telemetria/precipitacion/consulta', views.consulta_precipitacion, name='consulta_precipitacion'),

    re_path(r'telemetria/multiestacion_precipitacion/$', views.PrecipitacionMultiestacionView.as_view(),
            name='multiestacion_precipitacion'),

    # urls para el CRUD del modelo ConfigVisualizar
    re_path(r'telemetria/visualizar/config/$', views.ConfigVisualizarList.as_view(), name='configvisualizar_list'),
    path('telemetria/json/', views.ConfigVisualizarJson.as_view(), name='json'),
    path('configvisualizar/create/', views.ConfigVisualizarCreate.as_view(), name='configvisualizar_create'),
    path('configvisualizar/detail/<int:pk>/', views.ConfigVisualizarDetail.as_view(), name='configvisualizar_detail'),
    path('configvisualizar/edit/<int:pk>/', views.ConfigVisualizarUpdate.as_view(), name='configvisualizar_update'),
    path('configvisualizar/<int:pk>/delete/', views.ConfigVisualizarDelete.as_view(), name='configvisualizar_delete'),


    re_path(r'telemetria/alarma_transmision/config/$', views.ConfigAlarmaList.as_view(),
            name='config_alarma_list'),
    re_path(r'telemetria/alarma_transmision_limites/$', views.ConfigAlarmaTransmisionLimites.as_view(),
            name='config_alarma_transmision_limites'),
    re_path(r'telemetria/alarma_email/config/create/$', views.ConfigAlarmaEmailCreate.as_view(),
            name='config_alarma_email_create'),
    re_path(r'telemetria/alarma_email/config/delete/(?P<pk>\d+)/$', views.ConfigAlarmaEmailDelete.as_view(),
            name='config_alarma_email_delete'),

    re_path(r'telemetria/mapa/alarma_transmision$', views.MapaTransmision.as_view(), name='mapa_alarma_transmision'),
    re_path(r'^ajax/telemetria/mapa_alarma_transmision', views.MapaTransmisionConsulta, name='consulta_mapa_alarma_transmision'),
]
