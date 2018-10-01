from django.urls import re_path,path
from . import views

from django.contrib.auth import views as auth_views

app_name = 'medicion'
urlpatterns = [
    re_path(r'^medicion/$', views.MedicionList.as_view(), name='medicion_index'),
    re_path(r'^medicion/listdelete/$', views.ListDelete.as_view(), name='list_delete'),
    re_path(r'^medicion/filter/$', views.MedicionFilter.as_view(), name='medicion_filter'),
    re_path(r'^medicion/filterdelete/$', views.FilterDelete.as_view(), name='filter_delete'),
    re_path(r'medicion/create/$', views.MedicionCreate.as_view(), name='medicion_create'),
    re_path(r'medicion/(?P<pk>[0-9]+)/(?P<fecha>[0-9-]+)/(?P<var_id>[0-9]+)/$', views.MedicionUpdate.as_view(),
         name='medicion_update'),
    re_path(r'medicion/delete/(?P<pk>[0-9]+)/(?P<fecha>[0-9-]+)/(?P<var_id>[0-9]+)/$', views.MedicionDelete.as_view(),
         name='medicion_delete'),
    path('medicion/consulta/', views.MedicionConsulta.as_view(), name='medicion_consulta'),
    # re_path(r'medicion/importacion/(?P<imp_id>[0-9]+)/$', views.MedicionImportacion.as_view(),
    # name='medicion_importacion'),
    path('medicion/curvadescarga/', views.CurvaDescargaList.as_view(), name='curvadescarga_index'),
    path('medicion/curvadescarga/<int:page>/', views.CurvaDescargaList.as_view(), name='curvadescarga_index'),
    path('medicion/curvadescarga/create/', views.CurvaDescargaCreate.as_view(), name='curvadescarga_create'),
    path('medicion/curvadescarga/detail/<int:pk>/', views.CurvaDescargaDetail.as_view(), name='curvadescarga_detail'),
    path('medicion/curvadescarga/edit/<int:pk>/', views.CurvaDescargaUpdate.as_view(), name='curvadescarga_update'),
    path('medicion/curvadescarga/<int:pk>/delete/', views.CurvaDescargaDelete.as_view(), name='curvadescarga_delete'),
]
