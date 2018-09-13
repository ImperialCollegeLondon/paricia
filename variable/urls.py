from django.urls import re_path,path
from . import views

app_name = 'variable'
urlpatterns = [
    re_path(r'^variable/$', views.VariableList.as_view(), name='variable_index'),
    path('variable/<int:page>/', views.VariableList.as_view(), name='variable_index'),
    re_path(r'variable/create/$', views.VariableCreate.as_view(), name='variable_create'),
    re_path(r'variable/detail/(?P<pk>[0-9]+)/$', views.VariableDetail.as_view(), name='variable_detail'),
    path('variable/edit/<int:pk>/', views.VariableUpdate.as_view(), name='variable_update'),
    re_path(r'variable/(?P<pk>[0-9]+)/delete/$', views.VariableDelete.as_view(), name='variable_delete'),

    path('unidad/', views.UnidadList.as_view(), name='unidad_index'),
    path('unidad/<int:page>/', views.UnidadList.as_view(), name='unidad_index'),
    re_path(r'unidad/create/$', views.UnidadCreate.as_view(), name='unidad_create'),
    path('unidad/detail/<int:pk>/', views.UnidadDetail.as_view(), name='unidad_detail'),
    path('unidad/edit/<int:pk>/', views.UnidadUpdate.as_view(), name='unidad_update'),
    re_path(r'unidad/(?P<pk>[0-9]+)/delete/$', views.UnidadDelete.as_view(), name='unidad_delete'),

    re_path(r'control/$', views.ControlList.as_view(), name='control_index'),
    re_path(r'control/(?P<page>[0-9]+)/$', views.ControlList.as_view(), name='control_index'),
    re_path(r'control/create/$', views.ControlCreate.as_view(), name='control_create'),
    re_path(r'control/detail/(?P<pk>[0-9]+)/$', views.ControlDetail.as_view(), name='control_detail'),
    re_path(r'control/edit/(?P<pk>[0-9]+)/$', views.ControlUpdate.as_view(), name='control_update'),
    re_path(r'control/(?P<pk>[0-9]+)/delete/$', views.ControlDelete.as_view(), name='control_delete'),

]
