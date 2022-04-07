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

from excel_response import ExcelResponse


def excel_estacion(estaciones):
    cabecera = [
        [
            "Código",
            "Descripción",
            "Tipo",
            "País",
            "Región",
            "Ecosistema",
            "Socio",
            "Sitio",
            "Cuenca",
            "Latitud",
            "Longitud",
            "Altura",
            "Estado",
        ],
    ]
    cuerpo = []
    for objeto in estaciones:
        fila = []
        fila.append(objeto.est_codigo)
        fila.append(objeto.est_nombre)
        fila.append(objeto.tipo.nombre if objeto.tipo is not None else None)
        fila.append(objeto.pais.nombre if objeto.pais is not None else None)
        fila.append(objeto.region.nombre if objeto.region is not None else None)
        fila.append(objeto.ecosistema.nombre if objeto.ecosistema is not None else None)
        fila.append(objeto.socio.nombre if objeto.socio is not None else None)
        try:
            fila.append(objeto.sitiocuenca.sitio.nombre)
        except:
            fila.append(None)
        try:
            fila.append(objeto.sitiocuenca.cuenca.nombre)
        except:
            fila.append(None)
        fila.append(objeto.est_latitud)
        fila.append(objeto.est_longitud)
        fila.append(objeto.est_altura)
        fila.append("Operativa" if objeto.est_estado else "No operativa")
        cuerpo.append(fila)
    response = ExcelResponse(cabecera + cuerpo, "Estaciones_iMHEA")
    return response
