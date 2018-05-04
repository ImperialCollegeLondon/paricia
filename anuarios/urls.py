# -*- coding: utf-8 -*-
from django.urls import re_path
from anuarios import views

app_name = 'anuarios'
urlpatterns = [
    # url(r'^anuarios/$',views.ValidacionList.as_view(),name='validacion_index'),
    re_path('anuarios/procesar/', views.ProcesarVariables.as_view(), name='anuarios_procesar'),
    re_path(r'^anuarios/variables', views.lista_variables, name='anuarios_variables'),

]
