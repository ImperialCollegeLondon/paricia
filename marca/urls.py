from django.urls import re_path
from marca import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'marca'
urlpatterns = [
    re_path(r'marca/$', views.MarcaList.as_view(), name='marca_index'),
    re_path(r'marca/(?P<page>[0-9]+)/$', views.MarcaList.as_view(), name='marca_index'),
    re_path(r'marca/create/$', views.MarcaCreate.as_view(), name='marca_create'),
    re_path(r'marca/detail/(?P<pk>[0-9]+)/$', views.MarcaDetail.as_view(), name='marca_detail'),
    re_path(r'marca/update/(?P<pk>[0-9]+)/$', views.MarcaUpdate.as_view(), name='marca_update'),
    re_path(r'marca/(?P<pk>[0-9]+)/delete/$', views.MarcaDelete.as_view(), name='marca_delete'),

]
