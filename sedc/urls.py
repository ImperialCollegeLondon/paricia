"""sedc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  re_path(r'^blog/', include('blog.urls'))
"""

from django.urls import re_path, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  re_path(r'^admin/', admin.site.urls),
                  # re_path(r'^$', TemplateView.as_view(template_name="home.html")),
                  re_path(r'^', include('home.urls', namespace='home')),
                  re_path(r'^', include('reportes.urls', namespace='reportes')),
                  re_path(r'^', include('datalogger.urls', namespace='datalogger')),
                  re_path(r'^', include('estacion.urls', namespace='estacion')),
                  re_path(r'^', include('variable.urls', namespace='variable')),
                  re_path(r'^', include('formato.urls', namespace='formato')),
                  re_path(r'^', include('medicion.urls', namespace='medicion')),
                  re_path(r'^', include('vacios.urls', namespace='vacios')),
                  re_path(r'^', include('frecuencia.urls', namespace='frecuencia')),
                  re_path(r'^', include('importacion.urls', namespace='importacion')),
                  re_path(r'^', include('marca.urls', namespace='marca')),
                  re_path(r'^', include('validacion.urls', namespace='validacion')),
                  re_path(r'^', include('anuarios.urls', namespace='anuarios')),
                  re_path(r'^', include('sensor.urls', namespace='sensor')),
                  re_path(r'^', include('instalacion.urls', namespace='instalacion')),
                  re_path(r'^', include('bitacora.urls', namespace='bitacora')),
                  re_path(r'^', include('cruce.urls', namespace='cruce')),
                  re_path(r'^', include('registro.urls', namespace='registro')),
                  re_path('^', include('django.contrib.auth.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
