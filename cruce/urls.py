from django.urls import re_path, include

from cruce import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'cruce'
urlpatterns = [
    re_path(r'cruce/$', views.CruceList.as_view(), name='cruce_index'),
    re_path(r'cruce/(?P<page>[0-9]+)/$', views.CruceList.as_view(), name='cruce_index'),
    re_path(r'cruce/create/$', views.CruceCreate.as_view(), name='cruce_create'),
    re_path(r'cruce/detail/(?P<pk>[0-9]+)/$', views.CruceDetail.as_view(), name='cruce_detail'),
    re_path(r'cruce/edit/(?P<pk>[0-9]+)/$', views.CruceUpdate.as_view(), name='cruce_update'),
    re_path(r'cruce/(?P<pk>[0-9]+)/delete/$', views.CruceDelete.as_view(), name='cruce_delete'),

]
