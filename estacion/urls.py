from django.urls import re_path, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'estacion'
urlpatterns = [
    path('estacion/', views.EstacionList.as_view(), name='estacion_index'),
    path('estacion/json/', views.EstacionListJson.as_view(), name='json'),
    path('estacion/filter/', views.EstacionFilter.as_view(), name='filter'),
    path('estacion/<int:page>/', views.EstacionList.as_view(), name='estacion_index'),
    path('estacion/create/', views.EstacionCreate.as_view(), name='estacion_create'),
    path('estacion/detail/<int:pk>/', views.EstacionDetail.as_view(), name='estacion_detail'),
    path('estacion/edit/<int:pk>/', views.EstacionUpdate.as_view(), name='estacion_update'),
    path('estacion/<int:pk>/delete/', views.EstacionDelete.as_view(), name='estacion_delete'),
    path('estacion/getjson', views.datos_json_estaciones, name='jsonestaciones'),
    path('estacion/getjsoninamhi', views.estaciones_inamhi_json, name='jsonestacionesinamhi'),
    path('estacion/search', views.search_estaciones, name='search_estaciones'),
    # path('marca/',views.MarcaList.as_view(),name='marca_index'),
]
