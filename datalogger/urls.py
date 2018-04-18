from django.urls import re_path, include
from datalogger import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'datalogger'
urlpatterns = [
    re_path(r'datalogger/$', views.DataloggerList.as_view(), name='datalogger_index'),
    re_path(r'datalogger/(?P<page>[0-9]+)/$', views.DataloggerList.as_view(), name='datalogger_index'),
    re_path(r'datalogger/create/$', views.DataloggerCreate.as_view(), name='datalogger_create'),
    re_path(r'datalogger/detail/(?P<pk>[0-9]+)/$', views.DataloggerDetail.as_view(), name='datalogger_detail'),
    re_path(r'datalogger/edit/(?P<pk>[0-9]+)/$', views.DataloggerUpdate.as_view(), name='datalogger_update'),
    re_path(r'datalogger/(?P<pk>[0-9]+)/delete/$', views.DataloggerDelete.as_view(), name='datalogger_delete'),

]
