from django.urls import re_path,path
from . import views
# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib.auth import views as auth_views

app_name = 'vacios'
urlpatterns = [
    re_path(r'vacios/$', views.VaciosList.as_view(), name='vacios_index'),
    re_path(r'vacios/(?P<page>[0-9]+)/$', views.VaciosList.as_view(), name='vacios_index'),
    re_path(r'vacios/create/$', views.VaciosCreate.as_view(), name='vacios_create'),
    re_path(r'vacios/detail/(?P<pk>[0-9]+)/$', views.VaciosDetail.as_view(), name='vacios_detail'),
    re_path(r'vacios/edit/(?P<pk>[0-9]+)/$', views.VaciosUpdate.as_view(), name='vacios_update'),
    re_path(r'vacios/(?P<pk>[0-9]+)/delete/$', views.VaciosDelete.as_view(), name='vacios_delete'),
    path('vacios/dias/', views.DiasVacios.as_view(), name='dias'),
    # re_path(r'vacios/dias/$', views.DiasVacios.as_view(), name='dias'),
]
