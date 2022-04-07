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

from django.urls import re_path

from bitacora import views

app_name = "bitacora"
urlpatterns = [
    re_path(r"bitacora/$", views.BitacoraList.as_view(), name="bitacora_index"),
    re_path(
        r"bitacora/create/$", views.BitacoraCreate.as_view(), name="bitacora_create"
    ),
    re_path(
        r"bitacora/detail/(?P<pk>[0-9]+)/$",
        views.BitacoraDetail.as_view(),
        name="bitacora_detail",
    ),
    re_path(
        r"bitacora/edit/(?P<pk>[0-9]+)/$",
        views.BitacoraUpdate.as_view(),
        name="bitacora_update",
    ),
    re_path(
        r"bitacora/(?P<pk>[0-9]+)/delete/$",
        views.BitacoraDelete.as_view(),
        name="bitacora_delete",
    ),
]
