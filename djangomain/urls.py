########################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos
# (iMHEA)basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#           Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS),
#           Ecuador.
#           Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones
#  creadoras, ya sea en uso total o parcial del código.
########################################################################################

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
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from management.views import RegisterUserAPIView

from .views import HomePageView, schema_view

urlpatterns = [
    path("", HomePageView.as_view()),
    path("admin/", admin.site.urls),
    path("auth/", include("django.contrib.auth.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("register/", RegisterUserAPIView.as_view(), name="auth_register"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("station/", include("station.urls", namespace="station")),
    path("sensor/", include("sensor.urls", namespace="sensor")),
    path("variable/", include("variable.urls", namespace="variable")),
    path("formatting/", include("formatting.urls", namespace="formatting")),
    path("measurement/", include("measurement.urls", namespace="measurement")),
    path("importing/", include("importing.urls", namespace="importing")),
    path("management/", include("management.urls", namespace="management")),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger"),
        name="schema-swagger-ui",
    ),
    re_path(r"^redoc/$", schema_view.with_ui("redoc"), name="schema-redoc"),
]

urlpatterns += [
    path("api-auth/", include("rest_framework.urls")),
]

if settings.DEBUG:
    #
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #
    # import debug_toolbar
    # urlpatterns = [
    #     path('__debug__/', include(debug_toolbar.urls)),
    # ] + urlpatterns
