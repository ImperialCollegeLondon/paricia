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

from validacion import views

app_name = "validacion"
urlpatterns = [
    re_path(r"^validacion/$", views.ValidacionList.as_view(), name="validacion_index"),
    re_path(
        r"^validacion/(?P<page>[0-9]+)/$",
        views.ValidacionList.as_view(),
        name="validacion_index",
    ),
    re_path(
        r"^validacion/detail/(?P<pk>[0-9]+)/$",
        views.ValidacionDetail.as_view(),
        name="validacion_detail",
    ),
    re_path(r"^validacion/validar/$", views.Validar.as_view(), name="validar"),
    re_path(
        r"^validacion/periodos_validacion/$",
        views.PeriodosValidacion.as_view(),
        name="periodos_validacion",
    ),
    re_path(
        r"^validacion/borrar_validados/$",
        views.BorrarValidados.as_view(),
        name="borrar_validados",
    ),
    re_path(
        r"^validacion/borrar_crudos_y_validados/$",
        views.BorrarCrudosYValidados.as_view(),
        name="borrar_crudos_y_validados",
    ),
    re_path(
        r"^validacion/calidad/validar/$",
        views.CalidadValidar.as_view(),
        name="calidad_validar",
    ),
    re_path(
        r"^validacion/calidad/periodos_validacion/$",
        views.CalidadPeriodosValidacion.as_view(),
        name="calidad_periodos_validacion",
    ),
    re_path(
        r"^validacion/calidad/borrar_datos/$",
        views.CalidadBorrarDatos.as_view(),
        name="calidad_borrar_datos",
    ),
    re_path(
        r"^ajax/validacion/profundidades",
        views.view_profundidades,
        name="profundidades",
    ),
    re_path(
        r"^ajax/validacion_enviar", views.validacion_enviar, name="validacion_enviar"
    ),
]
