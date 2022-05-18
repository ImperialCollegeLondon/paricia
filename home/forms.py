# -*- coding: utf-8 -*-

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

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=25)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)


OPCIONES_CARGA = [
    ("variable_unidad.json", "VARIABLE: Unidades"),
    ("variable_variable.json", "VARIABLE: Lista de variables"),
    ("formato_delimitador.json", "FORMATO: Delimitadores"),
    ("formato_extension.json", "FORMATO: Extensiones de archivo"),
    ("formato_fecha.json", "FORMATO: Fecha"),
    ("formato_hora.json", "FORMATO: Hora"),
    ("formato_formato.json", "FORMATO: Formato de importación"),
    ("formato_clasificacion.json", "FORMATO: Clasificación"),
    # ("frecuencia_tipofrecuencia.json", "FRECUENCIA: Tipo"),
    # ("telemetria_alarmatipoestado.json", "TELEMETRÍA: Estados de alarma"),
    ("sensor_marca.json", "SENSOR: Marca"),
    ("sensor_tipo.json", "SENSOR: Tipo"),
    # ("datalogger_marca.json", "DATALOGGER: Marca"),
    ("estacion_tipo.json", "ESTACIÓN: Tipo"),
    ("estacion_ecosistema.json", "ESTACIÓN: Ecosistema"),
    ("estacion_pais.json", "ESTACIÓN: País"),
    ("estacion_region.json", "ESTACIÓN: Región"),
    ("estacion_sitio.json", "ESTACIÓN: Sitio"),
    ("estacion_cuenca.json", "ESTACIÓN: Cuenca"),
    ("estacion_sitiocuenca.json", "ESTACIÓN: Asociación Sitio-Cuenca"),
    ("estacion_socio.json", "ESTACIÓN: Socio"),
    ("estacion_estacion.json", "ESTACIÓN: Estación"),
    ("formato_asociacion.json", "FORMATO/ESTACION: Asociación de Formato con Estación"),
    ("cruce_cruce.json", "VARIABLE/ESTACION: Asociación Variable por Estación"),
    # (
    #    "frecuencia_frecuencia.json",
    #    "FRECUENCIA/VARIABLE/ESTACION: Frecuencias por variable y por estación",
    # ),
]


class CargaInicialForm(forms.Form):
    tabla = forms.ChoiceField(
        label="Seleccione tabla a cargar",
        choices=OPCIONES_CARGA,
        widget=forms.RadioSelect,
    )
