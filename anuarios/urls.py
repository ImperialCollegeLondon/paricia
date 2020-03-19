# -*- coding: utf-8 -*-
from django.urls import re_path, path
from anuarios import views

app_name = 'anuarios'
urlpatterns = [
    # url(r'^anuarios/$',views.ValidacionList.as_view(),name='validacion_index'),
    path('anuarios/procesar/', views.ProcesarVariables.as_view(), name='anuarios_procesar'),
    # path('anuarios/variables/', views.lista_variables, name='anuarios_variables'),
    path('anuarios/variables/<int:estacion>', views.lista_variables, name='anuarios_variables'),

]
