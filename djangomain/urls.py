################################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos (iMHEA)
# basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#         Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS), Ecuador.
#         Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones creadoras,
#              ya sea en uso total o parcial del código.

"""djangomain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("django.contrib.auth.urls")),
    path("", include("home.urls", namespace="home")),
    path("", include("estacion.urls", namespace="estacion")),
    path("", include("datalogger.urls", namespace="datalogger")),
    path("", include("sensor.urls", namespace="sensor")),
    path("", include("variable.urls", namespace="variable")),
    path("", include("bitacora.urls", namespace="bitacora")),
    path("", include("cruce.urls", namespace="cruce")),
    path("", include("formato.urls", namespace="formato")),
    path("", include("frecuencia.urls", namespace="frecuencia")),
    path("", include("instalacion.urls", namespace="instalacion")),
    path("", include("medicion.urls", namespace="medicion")),
    path("", include("validacion.urls", namespace="validacion")),
    path("", include("importacion.urls", namespace="importacion")),
    path("", include("vacios.urls", namespace="vacios")),
    path("", include("calidad.urls", namespace="calidad")),
    path("", include("reportes.urls", namespace="reportes")),
    path("", include("reportes_v2.urls", namespace="reportes_v2")),
    path("", include("telemetria.urls", namespace="telemetria")),
    path("", include("indices.urls", namespace="indices")),
    path("", include("validacion_v2.urls", namespace="validacion_v2")),
    path("", include("anuarios.urls", namespace="anuarios")),
]

if settings.DEBUG:
    #
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #
    # import debug_toolbar
    # urlpatterns = [
    #     path('__debug__/', include(debug_toolbar.urls)),
    # ] + urlpatterns
