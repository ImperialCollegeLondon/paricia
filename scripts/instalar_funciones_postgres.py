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


"""Installation script for POSTGRES function
Creates functions in the database needed for several activities such as:
    - Data types needed for validation and import function
    - Store raw data to validated table after quality check process.
    - Compute flow data from water level using a multilevel transfer function
    - Compute a report to show in data quality control interface
    - Compute hourly data from 5, 10, 30 min data
    - Compute daily data from hourly data
    - Compute monthly data from daily data

Use:
(venv)  $ python manage.py runscript instalar_funciones_postgres
(venv)  $ python manage.py shell <  ./scripts/instalar_funciones_postgres.py

"""

"""
Struct to translate variable_id to its name
The third parameter is a boolean to identify if a variable is treated as:
    - (TRUE) Accumulated -> Precipitation
    - (FALSE) Averaged -> Temperature, Air humidity, flow
    
    Parameters:
        id, nombre, es_acumulada(True)/es_promediada(False)
"""
vars = [
    [1, "precipitacion", True],
    [2, "temperaturaambiente", False],
    [3, "humedadrelativa", False],
    [4, "velocidadviento", False],
    [5, "direccionviento", False],
    [6, "humedadsuelo", False],
    [7, "radiacionsolar", False],
    [8, "presionatmosferica", False],
    [9, "temperaturaagua", False],
    [10, "caudal", False],
    [11, "nivelagua", False],
    [12, "voltajebateria", False],
    [13, "caudalaforo", False],
    [14, "nivelregleta", False],
    [15, "direccionvientorafaga", True],
    [16, "recorridoviento", False],
    [17, "gustdir", False],
    [18, "gusth", False],
    [19, "gustm", False],
    [20, "temperaturasuelo", False],
    [21, "radiacionindirecta", False],
    [22, "radiacionsolarsuma", True],
]

vars_profundidad = [
    [101, "temperaturaaguaprofundidad", False],
    [102, "ph", False],
    [103, "potencialredox", False],
    [104, "turbidez", False],
    [105, "clorofila", False],
    [106, "oxigenodisuelto", False],
    [107, "porcentajeoxigenodisuelto", False],
    [108, "ficocianina", False],
]


from django.db import connection


def insercion_validacion():
    """
    - Installs POSTGRES data type needed for 'importacion' app
        scripts/plpgsql/insertar_validacion_requisitos.sql:

    - Installs POSTGRES data type needed for 'validacion' app
        scripts/plpgsql/insertar_1validacion.sql:

    """
    print("Funciones para insercion datos a VALIDACION ")
    file0 = open("scripts/plpgsql/insertar_validacion_requisitos.sql", "r")
    sql0 = file0.read()
    with connection.cursor() as cursor:
        cursor.execute(sql0)

    file = open("scripts/plpgsql/insertar_1validacion.sql", "r")
    funcion = file.read()
    for var in vars:
        var_id = str(var[0])
        sql = funcion.replace("1", var_id)
        with connection.cursor() as cursor:
            cursor.execute(sql)


def inserccion_validacion_profundidad():
    """
    - Installs POSTGRES data type needed for 'importacion' app (data with depth)
        scripts/plpgsql/insertar_validacion_requisitos.sql:

    - Installs POSTGRES data type needed for 'validacion' app (data with depth)
        scripts/plpgsql/insertar_1validacion.sql:

    """
    print("Funciones para insercion datos a VALIDACION con profundidad ")
    file0 = open("scripts/plpgsql/insertar_validacion_requisitos.sql", "r")
    sql0 = file0.read()
    with connection.cursor() as cursor:
        cursor.execute(sql0)

    file = open("scripts/plpgsql/insertar_101validacion_profundidad.sql", "r")
    funcion = file.read()
    for var in vars_profundidad:
        var_id = str(var[0])
        sql = funcion.replace("101", var_id)
        with connection.cursor() as cursor:
            cursor.execute(sql)


def aplicar_curvadescarga():
    """
    Installs POSTGRES functions needed to compute FLOW from WATER LEVEL
    The computation is triggered after WATER LEVEL is validated
        (When WATER LEVEL goes from raw to validated tables)
    """
    print("Trigger curva de descarga")
    file = open("scripts/plpgsql/aplicar_curva_descarga.sql", "r")
    sql = file.read()
    with connection.cursor() as cursor:
        cursor.execute(sql)


def aplicar_curvadescarga_crudos():
    """
    Installs POSTGRES functions needed to compute FLOW from WATER LEVEL
    The computation is triggered after new data is stored in raw WATER LEVEL table.
    """
    print("Trigger curva de descarga crudos")
    file = open("scripts/plpgsql/aplicar_curva_descarga_crudos.sql", "r")
    sql = file.read()
    with connection.cursor() as cursor:
        cursor.execute(sql)


def calculo_caudal():
    """
    Installs POSTGRES functions needed to compute FLOW from WATER LEVEL
    The computation is triggered after a transfer function have changed
    """
    print("Trigger Cálculo caudal")
    file = open("scripts/plpgsql/calculo_caudal.sql", "r")
    sql = file.read()
    with connection.cursor() as cursor:
        cursor.execute(sql)


def reporte_validacion():
    """
    Installs a POSTGRES function to get a report with several calculations to make quality check
    """
    print("Funciones Reporte validacion")
    file = open("scripts/plpgsql/reporte_validacion.sql", "r")
    sql_base = file.read()
    for var in vars:
        var_id = str(var[0])
        sql = sql_base.replace("%%var_id%%", var_id)
        with connection.cursor() as cursor:
            cursor.execute(sql)


def reporte_validacion_profundidad():
    """
    Installs a POSTGRES function to get a report with several calculations to make quality check
        with variables with depth
    """
    print("Funciones Reporte validacion para variables con profundidad")
    file = open("scripts/plpgsql/reporte_validacion_profundidad.sql", "r")
    sql_base = file.read()
    for var in vars_profundidad:
        var_id = str(var[0])
        sql = sql_base.replace("var101", "var" + var_id)
        sql = sql.replace("var_id = 101", "var_id = " + var_id)
        with connection.cursor() as cursor:
            cursor.execute(sql)


def generar_horario():
    """
    Installs a POSTGRES function to compute HOURLY data from 5,10,30 min data

    When a variable is set to 'is_accumulated = TRUE' (as precipitation) it uses
        `scripts/plpgsql/generar_horario_acum.sql`

    When a variable is set to 'is_accumulated = FALSE' (as temperature -> averaged) it uses
        `scripts/plpgsql/generar_horario_prom.sql`
    """
    print("Funciones generar Horario")
    file_acum = open("scripts/plpgsql/generar_horario_acum.sql", "r")
    sql_acum = file_acum.read()
    file_prom = open("scripts/plpgsql/generar_horario_prom.sql", "r")
    sql_prom = file_prom.read()

    for var in vars:
        var_id = str(var[0])
        es_acumulada = var[2]

        if es_acumulada:
            sql = sql_acum
            sql = sql.replace("var1", "var" + var_id)
            sql = sql.replace("f.var_id_id = 1", "f.var_id_id = " + var_id)
            sql = sql.replace("var_id = 1", "var_id = " + var_id)
        else:
            sql = sql_prom
            sql = sql.replace("var2", "var" + var_id)
            sql = sql.replace("f.var_id_id = 2", "f.var_id_id = " + var_id)
            sql = sql.replace("var_id = 2", "var_id = " + var_id)

        with connection.cursor() as cursor:
            cursor.execute(sql)


def generar_horario_profundidad():
    """
    Installs a POSTGRES function to compute HOURLY data from 5,10,30 minute data with depth

    When a variable is set to 'is_accumulated = TRUE' (as precipitation) it uses
        `scripts/plpgsql/generar_horario_acum.sql`

    When a variable is set to 'is_accumulated = FALSE' (as temperature -> averaged) it uses
        `scripts/plpgsql/generar_horario_prom.sql`
    """
    print("Funciones generar Horario profundidad")
    file_prom = open("scripts/plpgsql/generar_horario_prom_profundidad.sql", "r")
    sql_prom = file_prom.read()

    for var in vars_profundidad:
        var_id = str(var[0])
        es_acumulada = var[2]

        if es_acumulada:
            continue
            # sql = sql_acum.replace('var_id_id = 1', 'var_id_id = ' + var_id)
            # sql = sql.replace('var1', 'var' + var_id)
        else:
            sql = sql_prom.replace("101", var_id)

        with connection.cursor() as cursor:
            cursor.execute(sql)


def generar_diario():
    """
    Installs a POSTGRES function to compute DAILY data from HOURLY data

    When a variable is set to 'is_accumulated = TRUE' (as precipitation) it uses
        `scripts/plpgsql/generar_diario_acum.sql`

    When a variable is set to 'is_accumulated = FALSE' (as temperature -> averaged) it uses
        `scripts/plpgsql/generar_diario_prom.sql`
    """
    print("Funciones Generar Diario")
    file_acum = open("scripts/plpgsql/generar_diario_acum.sql", "r")
    sql_acum = file_acum.read()
    file_prom = open("scripts/plpgsql/generar_diario_prom.sql", "r")
    sql_prom = file_prom.read()

    for var in vars:
        var_id = str(var[0])
        es_acumulada = var[2]

        if es_acumulada:
            sql = sql_acum.replace("var_id = 1", "var_id = " + var_id)
            sql = sql.replace("var1", "var" + var_id)
        else:
            sql = sql_prom.replace("var_id = 2", "var_id = " + var_id)
            sql = sql.replace("var2", "var" + var_id)

        with connection.cursor() as cursor:
            cursor.execute(sql)


def generar_diario_profundidad():
    """
    Installs a POSTGRES function to compute DAILY data from HOURLY data with depth

    When a variable is set to 'is_accumulated = TRUE' (as precipitation) it uses
        `scripts/plpgsql/generar_diario_acum.sql`

    When a variable is set to 'is_accumulated = FALSE' (as temperature -> averaged) it uses
        `scripts/plpgsql/generar_diario_prom.sql`
    """
    print("Funciones Generar Diario Profundidad")
    # file_acum = open("scripts/plpgsql/generar_acum.sql", 'r')
    # sql_acum = file_acum.read()
    file_prom = open("scripts/plpgsql/generar_diario_prom_profundidad.sql", "r")
    sql_prom = file_prom.read()

    for var in vars_profundidad:
        var_id = str(var[0])
        es_acumulada = var[2]

        if es_acumulada:
            continue
            # sql = sql_acum.replace('var_id = 1', 'var_id = ' + var_id)
            # sql = sql.replace('var1', 'var' + var_id)
        else:
            sql = sql_prom.replace("101", var_id)

        with connection.cursor() as cursor:
            cursor.execute(sql)


def generar_mensual():
    """
    Installs a POSTGRES function to compute MONTHLY data from DAILY data

    When a variable is set to 'is_accumulated = TRUE' (as precipitation) it uses
        `scripts/plpgsql/generar_mensual_acum.sql`

    When a variable is set to 'is_accumulated = FALSE' (as temperature -> averaged) it uses
        `scripts/plpgsql/generar_mensual_prom.sql`
    """
    print("Generar Mensual")
    file_acum = open("scripts/plpgsql/generar_mensual_acum.sql", "r")
    sql_acum = file_acum.read()
    file_prom = open("scripts/plpgsql/generar_mensual_prom.sql", "r")
    sql_prom = file_prom.read()

    for var in vars:
        var_id = str(var[0])
        es_acumulada = var[2]

        if es_acumulada:
            sql = sql_acum.replace("var_id = 1", "var_id = " + var_id)
            sql = sql.replace("var1", "var" + var_id)
        else:
            sql = sql_prom.replace("var_id = 2", "var_id = " + var_id)
            sql = sql.replace("var2", "var" + var_id)

        with connection.cursor() as cursor:
            cursor.execute(sql)


def generar_mensual_profundidad():
    """
    Installs a POSTGRES function to compute MONTHLY data from DAILY data with depth

    When a variable is set to 'is_accumulated = TRUE' (as precipitation) it uses
        `scripts/plpgsql/generar_mensual_acum.sql`

    When a variable is set to 'is_accumulated = FALSE' (as temperature -> averaged) it uses
        `scripts/plpgsql/generar_mensual_prom.sql`
    """
    print("Generar Mensual Profundidad")
    # file_acum = open("scripts/plpgsql/generar_mensual_acum.sql", 'r')
    # sql_acum = file_acum.read()
    file_prom = open("scripts/plpgsql/generar_mensual_prom_profundidad.sql", "r")
    sql_prom = file_prom.read()

    for var in vars_profundidad:
        var_id = str(var[0])
        es_acumulada = var[2]

        if es_acumulada:
            continue
            # sql = sql_acum.replace('var_id = 1', 'var_id = ' + var_id)
            # sql = sql.replace('var1', 'var' + var_id)
        else:
            sql = sql_prom.replace("101", var_id)

        with connection.cursor() as cursor:
            cursor.execute(sql)


def run():
    """
    Run the POSTGRES installation functions
    """
    reporte_validacion()
    reporte_validacion_profundidad()
    insercion_validacion()
    inserccion_validacion_profundidad()
    aplicar_curvadescarga()
    aplicar_curvadescarga_crudos()
    calculo_caudal()
    generar_horario()
    generar_diario()
    generar_mensual()
    generar_horario_profundidad()
    generar_diario_profundidad()
    generar_mensual_profundidad()
