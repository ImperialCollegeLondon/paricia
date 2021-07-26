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

menu_tab_html = """
<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" id="navbarInfoRed" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
    __PESTAÑA__
    </a>
    <div class="dropdown-menu" aria-labelledby="navbarDropdown">
        __ITEMS__
    </div>
</li>
"""

menu_item_html = """<a class="dropdown-item" href="__URL__">__NOMBRE__</a>"""
menu_item_divider_html = """<div class="dropdown-divider"></div>"""

menu_struct = [

    {
        "pestaña": "Estación",
        "permiso": "",
        "items": [
            {"nombre": "Estación", "url_name": "estacion:estacion_index", "permiso": "estacion.view_estacion"},
            {"nombre": "", },
            {"nombre": "País", "url_name": "estacion:pais_index", "permiso": "estacion.view_pais"},
            {"nombre": "Región/Provincia/Departamento", "url_name": "estacion:region_index", "permiso": "estacion.view_region"},
            {"nombre": "Ecosistema", "url_name": "estacion:ecosistema_index", "permiso": "estacion.view_ecosistema"},
            {"nombre": "Socio", "url_name": "estacion:socio_index", "permiso": "estacion.view_socio"},
            {"nombre": "Sitio", "url_name": "estacion:sitio_index", "permiso": "estacion.view_sitio"},
            {"nombre": "Cuenca", "url_name": "estacion:cuenca_index", "permiso": "estacion.view_cuenca"},
            {"nombre": "Asociación Sitio-Cuenca", "url_name": "estacion:sitiocuenca_index",
             "permiso": "estacion.view_sitiocuenca"},
            {"nombre": "Tipo de estación", "url_name": "estacion:tipo_index", "permiso": "estacion.view_tipo"},
        ]
    },

    {
        "pestaña": "Información de la red",
        "permiso": "",
        "items": [
            {"nombre": "Datalogger", "url_name": "datalogger:datalogger_index", "permiso": "datalogger.view_datalogger" },
            {"nombre": "Marca de datalogger", "url_name": "datalogger:marca_index", "permiso": "datalogger.view_marca" },
            {"nombre": "",},
            {"nombre": "Sensor", "url_name": "sensor:sensor_index", "permiso": "sensor.view_sensor" },
            {"nombre": "Marca de sensor", "url_name": "sensor:marca_index", "permiso": "sensor.view_marca" },
            {"nombre": "Tipo de sensor", "url_name": "sensor:tipo_index", "permiso": "sensor.view_tipo"},
            {"nombre": "",},
            {"nombre": "Frecuencia de Registro", "url_name": "frecuencia:frecuencia_index", "permiso": "frecuencia.view_frecuencia" },
            {"nombre": "Curva de descarga", "url_name": "medicion:curvadescarga_index", "permiso": "medicion.view_curvadescarga" },
            {"nombre": "", },
            {"nombre": "Unidad de variable", "url_name": "variable:unidad_index", "permiso": "variable.view_unidad" },
            {"nombre": "Variable", "url_name": "variable:variable_index", "permiso": "variable.view_variable" },
            {"nombre": "", },
            {"nombre": "Variables por Estación", "url_name": "cruce:cruce_index", "permiso": "cruce.view_cruce" },
        ]
    },

    {
        "pestaña": "Mantenimiento",
        "permiso": "",
        "items": [
            {"nombre": "Instalación de Sensor", "url_name": "variable:control_index", "permiso": "variable.view_control"},
            {"nombre": "Instalación de Datalogger", "url_name": "instalacion:instalacion_index", "permiso": "instalacion.view_instalacion"},
            {"nombre": "Historial", "url_name": "bitacora:bitacora_index", "permiso": "bitacora.view_bitacora"},
            {"nombre": "Carga inicial", "url_name": "home:carga_inicial", "permiso": "home.carga_inicial"},
        ]
    },

    {
        "pestaña": "Importación de datos",
        "permiso": "",
        "items": [
            {"nombre": "Importar Archivo", "url_name": "importacion:importacion_temp_create", "permiso": "importacion.add_importacion"},
            {"nombre": "Vacios de Información", "url_name": "vacios:vacios", "permiso": "vacios.view_vacios"},
            {"nombre": "Archivos Importados", "url_name": "importacion:importacion_index", "permiso": "importacion.view_importacion"},
            {"nombre": "", },
            {"nombre": "Formato de Importación", "url_name": "formato:formato_index", "permiso": "formato.view_formato"},
            {"nombre": "Formato por Estación", "url_name": "formato:asociacion_index", "permiso": "formato.view_asociacion"},
            {"nombre": "", },
            {"nombre": "Extensión de archivo", "url_name": "formato:extension_index", "permiso": "formato.view_extension"},
            {"nombre": "Delimitador de campos en archivo", "url_name": "formato:delimitador_index", "permiso": "formato.view_delimitador"},
            {"nombre": "Formato de Fecha", "url_name": "formato:fecha_index", "permiso": "formato.view_fecha"},
            {"nombre": "Formato de Hora", "url_name": "formato:hora_index", "permiso": "formato.view_hora"},
        ]
    },

    {
        "pestaña": "Validación",
        "permiso": "",
        "items": [
            {"nombre": "<small>HIDRO - </small>Validar Datos Crudos", "url_name": "validacion:validar", "permiso": "validacion.hidro_validar"},
            {"nombre": "<small>HIDRO - </small>Historial validaciones", "url_name": "validacion:validacion_index", "permiso": "validacion.view_validacion"},
            {"nombre": "", },
            {"nombre": "<small>HIDRO - </small>Borrar crudos y VALIDADOS", "url_name": "validacion:borrar_crudos_y_validados", "permiso": "validacion.hidro_borrar_crudos_y_validados"},
            {"nombre": "<small>HIDRO - </small>Borrar solo VALIDADOS", "url_name": "validacion:borrar_validados", "permiso": "validacion.hidro_borrar_solo_validados"},
            {"nombre": "", },
            {"nombre": "<small>LIMNO. - </small>Validar", "url_name": "validacion:calidad_validar", "permiso": "validacion.calidad_validar"},
            {"nombre": "<small>LIMNO. - </small>Borrar datos", "url_name": "validacion:calidad_borrar_datos", "permiso": "validacion.calidad_validar"},
        ]
    },
    {
        "pestaña": "Validación_v2",
        "permiso": "",
        "items": [
            {"nombre": "<small>HIDRO - </small>Validar Datos Crudos", "url_name": "validacion_v2:v2_diaria",
             "permiso": "validacion.hidro_validar"},
            {"nombre": "<small>HIDRO - </small>Historial validaciones", "url_name": "validacion:validacion_index",
             "permiso": "validacion.view_validacion"},
            {"nombre": "", },
        ]
    },
    {
        "pestaña": "Indices",
        "permiso": "",
        "items": [
            {"nombre": "Precipitación", "url_name": "indices:precipitacion", "permiso": "indices.view_indices"},
            {"nombre": "Intensidad - Duración", "url_name": "indices:intensidad", "permiso": "indices.view_indices"},
            {"nombre": "Intensidad - Duración Multiestación", "url_name": "indices:intensidadmulti", "permiso": "indices.view_indices"},
            {"nombre": "", },
            {"nombre": "Caudales", "url_name": "indices:caudal", "permiso": "indices.view_indices"},
            {"nombre": "Duración Caudal", "url_name": "indices:duracaudal", "permiso": "indices.view_indices"},
            {"nombre": "Duración Caudal Multiestación", "url_name": "indices:duracaudalmulti", "permiso": "indices.view_indices"},
            {"nombre": "", },
            {"nombre": "Coeficiente de Escorrentía", "url_name": "indices:escorrentia", "permiso": "indices.view_indices"},
        ]
    },




    {
        "pestaña": "Reportes",
        "permiso": "",
        "items": [
            {"nombre": "<small>HIDRO - </small>Consultas por Periodo", "url_name": "reportes:consultas_periodo", "permiso": "reportes.view_consultasperiodo"},
            {"nombre": "<small>HIDRO - </small>Diario", "url_name": "reportes:diario", "permiso": "reportes.view_diario"},
            {"nombre": "<small>HIDRO - </small>Mensual-Multianual", "url_name": "reportes:mensual_multianual", "permiso": "reportes.view_mensualmultianual"},
            {"nombre": "",},
            #{"nombre": "<small>HIDRO - </small>Anuario", "url_name": "reportes:anuario", "permiso": "reportes.view_anuario"},
            #{"nombre": "<small>HIDRO - </small>Procesar Anuario", "url_name": "anuarios:anuarios_procesar", "permiso": "reportes.view_anuario"},
            {"nombre": "<small>HIDRO - </small>Anuario", "url_name": "reportes_v2:anuario", "permiso": "reportes.view_anuario"},
            {"nombre": "<small>HIDRO - </small>Comparar 3 estaciones", "url_name": "reportes:comparacion_reporte", "permiso": "reportes.view_comparacionvalores"},
            {"nombre": "<small>HIDRO - </small>Comparar 2 variables", "url_name": "reportes:comparacion_variables", "permiso": "reportes.view_comparacionvariables"},
            {"nombre": "",},
            {"nombre": "<small>LIMNO. - </small>Gráfico: Serie temporal", "url_name": "calidad:grafico1", "permiso": "calidad.view_graficos"},
            {"nombre": "<small>LIMNO. - </small>Gráfico: Serie temporal CRUDOS", "url_name": "calidad:crudos_grafico1", "permiso": "calidad.view_graficoscrudos"},
            {"nombre": "<small>LIMNO. - </small>Gráfico: Promedio horario", "url_name": "calidad:grafico2", "permiso": "calidad.view_graficos"},
            {"nombre": "<small>LIMNO. - </small>Consulta Períodos", "url_name": "reportes:calidad_consultas_periodo", "permiso": "reportes.view_calidadconsultasperiodo"},
        ]
    },

    {
        "pestaña": "Telemetría",
        "permiso": "",
        "items": [
            {"nombre": "<small>HIDRO </small>Visualizar variables", "url_name": "telemetria:visualizar", "permiso": "telemetria.view_consulta"},
            {"nombre": "<small>LIMNO. </small>Visualizar variables", "url_name": "telemetria:calidad_visualizar", "permiso": "telemetria.view_calidad_consulta"},
            {"nombre": "Mapa transmisión", "url_name": "telemetria:mapa_alarma_transmision", "permiso": "telemetria.view_mapatransmision"},
            {"nombre": "Precipitación", "url_name": "telemetria:precipitacion", "permiso": "telemetria.view_precipitacion"},
            {"nombre": "Precipitación Multiestación", "url_name": "telemetria:multiestacion_precipitacion", "permiso": "telemetria.view_precipitacionmultiestacion"},
            {"nombre": "",},
            {"nombre": "<small>HIDRO </small>Configurar visualización", "url_name": "telemetria:configvisualizar_list", "permiso": "telemetria.add_configvisualizar"},
            {"nombre": "<small>LIMNO. </small>Configurar visualización", "url_name": "telemetria:configcalidad_list", "permiso": "telemetria.add_configcalidad"},
            {"nombre": "Configurar alarma", "url_name": "telemetria:config_alarma_list", "permiso": "telemetria.add_alarmaemail"},
        ]
    },

    {
        "pestaña": "Calidad de Agua",
        "permiso": "",
        "items": [
            {"nombre": "Gráfico comparación Limno. - Hidro", "url_name": "calidad:comparar_hidro", "permiso": "calidad.view_comparar_hidro"},
            {"nombre": "",},
            {"nombre": "Asociación estaciones Hidro", "url_name": "calidad:asociacionhidro_index", "permiso": "calidad.view_asociacionhidro"},
            {"nombre": "Permisos de usuario - variables", "url_name": "calidad:usuariovariable_index", "permiso": "calidad.view_usuariovariable"},
        ]
    },
]