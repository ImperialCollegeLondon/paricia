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

from reportes import views

app_name = "reportes"
urlpatterns = [
    re_path(r"^reportes/anuario/$", views.ReportesAnuario.as_view(), name="anuario"),
    re_path(
        r"^reportes/consultas/$",
        views.ConsultasPeriodo.as_view(),
        name="consultas_periodo",
    ),
    re_path(r"^reportes/diario/$", views.Diario.as_view(), name="diario"),
    re_path(
        r"^reportes/mensual_multianual/$",
        views.MensualMultianual.as_view(),
        name="mensual_multianual",
    ),
    re_path(
        r"^reportes/comparacion/$",
        views.ComparacionReporte.as_view(),
        name="comparacion_reporte",
    ),
    re_path(
        r"^reportes/comparacion_variables/$",
        views.ComparacionVariables.as_view(),
        name="comparacion_variables",
    ),
    re_path(r"^ajax/reportes_variables", views.variables, name="variables"),
    re_path(r"^ajax/reportes_cuencas", views.cuencas, name="cuencas"),
    re_path(r"^reportes/manual", views.manual, name="manual"),
    re_path(
        r"^reportes/calidad/consultas/$",
        views.CalidadConsultasPeriodo.as_view(),
        name="calidad_consultas_periodo",
    ),
    # # Utiliza un modelo antiguo "Medicion" muy posiblemente ya no se lo requiera
    # re_path(
    #     r'reportes/datos_horarios/(?P<est_id>[0-9]+)/(?P<var_id>[0-9]+)/(?P<fec_ini>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})/(?P<fec_fin>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})/$',
    #     views.datos_json_horarios, name='horarios'),
]
