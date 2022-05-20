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

from excel_response import ExcelResponse


def excel_station(stations):
    """
    Returns an Excel Spreadsheet given a queryset of Stations. Used to export
    information on stations in views.
    """

    header = [
        [
            "Code",
            "Description",
            "Station type",
            "Country",
            "Region",
            "Ecosystem",
            "Institution",
            "Place",
            "Basin",
            "Latitude",
            "Longitude",
            "Altitude",
            "State",
        ],
    ]
    body = []
    for obj in stations:
        line = []
        line.append(obj.station_code)
        line.append(obj.station_name)
        line.append(obj.station_type.name if obj.type is not None else None)
        line.append(obj.country.name if obj.country is not None else None)
        line.append(obj.region.name if obj.region is not None else None)
        line.append(obj.ecosystem.name if obj.ecosystem is not None else None)
        line.append(obj.institution.name if obj.institution is not None else None)
        try:
            line.append(obj.place_basin.place.name)
        except:
            line.append(None)
        try:
            line.append(obj.place_basin.basin.name)
        except:
            line.append(None)
        line.append(obj.station_latitude)
        line.append(obj.station_longitude)
        line.append(obj.station_altitude)
        line.append("Operational" if obj.station_state else "Not Operational")
        body.append(line)
    response = ExcelResponse(header + body, "Stations_iMHEA")
    return response
