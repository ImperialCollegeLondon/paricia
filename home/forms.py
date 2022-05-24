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
    ("variable_unit.json", "VARIABLE: Units"),
    ("variable_variable.json", "VARIABLE: List of variables"),
    ("formatting_delimiter.json", "FORMATTING: Delimiters"),
    ("formatting_extension.json", "FORMATTING: File extensions"),
    ("formatting_date.json", "FORMATTING: Date"),
    ("formatting_time.json", "FORMATTING: Time"),
    ("formatting_format.json", "FORMATTING: Import format"),
    ("formatting_classification.json", "FORMATTING: Classification"),
    # ("frecuencia_tipofrecuencia.json", "FRECUENCIA: Tipo"),
    # ("telemetria_alarmatipoestado.json", "TELEMETRÍA: Estados de alarma"),
    ("sensor_marca.json", "SENSOR: Marca"),
    ("sensor_tipo.json", "SENSOR: Tipo"),
    # ("datalogger_marca.json", "DATALOGGER: Marca"),
    ("station_stationtype.json", "STATION: StationType"),
    ("station_ecosystem.json", "STATION: Ecosystem"),
    ("station_country.json", "STATION: Country"),
    ("station_region.json", "STATION: Region"),
    ("station_place.json", "STATION: Place"),
    ("station_basin.json", "STATION: Basin"),
    ("station_placebasin.json", "STATION: Association Place-Basin"),
    ("station_institution.json", "STATION: Institution"),
    ("station_station.json", "STATION: Station"),
    ("format_association.json", "FORMATTING/STATION: Association Format-Station"),
]


class CargaInicialForm(forms.Form):
    tabla = forms.ChoiceField(
        label="Seleccione tabla a cargar",
        choices=OPCIONES_CARGA,
        widget=forms.RadioSelect,
    )
