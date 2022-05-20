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
    ("station_tipo.json", "STATION: Tipo"),
    ("station_ecosistema.json", "STATION: Ecosistema"),
    ("station_country.json", "STATION: País"),
    ("station_region.json", "STATION: Región"),
    ("station_sitio.json", "STATION: Sitio"),
    ("station_cuenca.json", "STATION: Cuenca"),
    ("station_sitiocuenca.json", "STATION: Asociación Sitio-Cuenca"),
    ("station_socio.json", "STATION: Socio"),
    ("station_station.json", "STATION: Station"),
    ("formato_asociacion.json", "FORMATO/ESTACION: Asociación de Formato con Station"),
    ("cruce_cruce.json", "VARIABLE/ESTACION: Asociación Variable por Station"),
]


class CargaInicialForm(forms.Form):
    tabla = forms.ChoiceField(
        label="Seleccione tabla a cargar",
        choices=OPCIONES_CARGA,
        widget=forms.RadioSelect,
    )
