from django.urls import re_path,path
from medicion import views

app_name = 'medicion'
urlpatterns = [

    re_path(r'^medicion/filter/$', views.MedicionFilter.as_view(), name='medicion_filter'),

    # re_path(r'medicion/importacion/(?P<imp_id>[0-9]+)/$', views.MedicionImportacion.as_view(),
    # name='medicion_importacion'),
    path('medicion/curvadescarga/', views.CurvaDescargaList.as_view(), name='curvadescarga_index'),
    path('medicion/curvadescarga/<int:page>/', views.CurvaDescargaList.as_view(), name='curvadescarga_index'),
    path('medicion/curvadescarga/create/', views.CurvaDescargaCreate.as_view(), name='curvadescarga_create'),
    path('medicion/curvadescarga/detail/<int:pk>/', views.CurvaDescargaDetail.as_view(), name='curvadescarga_detail'),
    path('medicion/curvadescarga/edit/<int:pk>/', views.CurvaDescargaUpdate.as_view(), name='curvadescarga_update'),
    path('medicion/curvadescarga/<int:pk>/delete/', views.CurvaDescargaDelete.as_view(), name='curvadescarga_delete'),

    path('medicion/datos_validacion/', views.lista_datos_validacion, name='lista_datos_validacion'),

    re_path(r'^ajax/medicion_variables', views.variables, name='variables'),
    re_path(r'^ajax/validacion_enviar', views.validacion_enviar, name='validacion_enviar'),


]
