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

# (venv)  $ python manage.py runscript instalar_funciones_postgres          ## Este comando requiere que este archivo esté dentro de scripts/
# (venv)  $ python manage.py shell <  ./scripts/instalar_funciones_postgres.py


from django.db import connection


######################################################################
##  Tipos de datos para inserccion
def inserccion_validacion():
    print("Funciones para inserccion datos a VALIDACION ")
    file_inserccion0 = open("scripts/plpgsql/inserccion0.sql", 'r')
    sql_inserccion0 = file_inserccion0.read()
    with connection.cursor() as cursor:
        cursor.execute(sql_inserccion0)

    file_inserccion1 = open("scripts/plpgsql/inserccion1.sql", 'r')
    funcion_inserccion1 = file_inserccion1.read()
    for var_id in range(1, 23):
        sql_inserccion = funcion_inserccion1.replace('1', str(var_id))
        with connection.cursor() as cursor:
            cursor.execute(sql_inserccion)


def inserccion_validacion_profundidad():
    print("Funciones para inserccion datos a VALIDACION con profundidad ")
    file_inserccion0 = open("scripts/plpgsql/inserccion0.sql", 'r')
    sql_inserccion0 = file_inserccion0.read()
    with connection.cursor() as cursor:
        cursor.execute(sql_inserccion0)

    file_inserccion1 = open("scripts/plpgsql/inserccion1_profundidad.sql", 'r')
    funcion_inserccion1 = file_inserccion1.read()
    for var_id in range(101, 108):
        sql_inserccion = funcion_inserccion1.replace('101', str(var_id))
        with connection.cursor() as cursor:
            cursor.execute(sql_inserccion)


####################################################################
# Crear funcion trigger: aplicar_curvadescarga      ## Esta función se aplica en la validación de NIVEL DE AGUA
def aplicar_curvadescarga():
    print("Trigger curva de descarga")
    file_curva_descarga = open("scripts/plpgsql/aplicar_curva_descarga.sql", 'r')
    sql_curva_descarga = file_curva_descarga.read()
    with connection.cursor() as cursor:
        cursor.execute(sql_curva_descarga)


####################################################################
# Crear funcion trigger: aplicar_curvadescarga_crudos      ## Esta función se aplica inserccion de datos en tabla NIVEL AGUA CRUDOS
def aplicar_curvadescarga_crudos():
    print("Trigger curva de descarga crudos")
    file_curva_descarga_crudos = open("scripts/plpgsql/aplicar_curva_descarga_crudos.sql", 'r')
    sql_curva_descarga_crudos = file_curva_descarga_crudos.read()
    with connection.cursor() as cursor:
        cursor.execute(sql_curva_descarga_crudos)



####################################################################
# Crear funcion trigger: calculo_caudal             ## Esta función se aplica cada vez que se cambia o actuliza un curva de descarga
def calculo_caudal():
    print("Trigger Cálculo caudal")
    file_calculo_caudal = open("scripts/plpgsql/calculo_caudal.sql", 'r')
    sql_calculo_caudal = file_calculo_caudal.read()
    with connection.cursor() as cursor:
        cursor.execute(sql_calculo_caudal)


def reporte_validacion():
    print("Funciones Reporte validacion")
    file_reporte_validacion = open("scripts/plpgsql/reporte_validacion.sql", 'r')
    sql_reporte_validacion = file_reporte_validacion.read()
    for var_id in range(1, 23):
        sql = sql_reporte_validacion.replace('%%var_id%%', str(var_id))
        with connection.cursor() as cursor:
            cursor.execute(sql)


def reporte_validacion_profundidad():
    print("Funciones Reporte validacion para variables con profundidad")
    file_reporte_validacion = open("scripts/plpgsql/reporte_validacion_profundidad.sql", 'r')
    sql_reporte_validacion = file_reporte_validacion.read()
    for var_id in range(101, 108):
        sql = sql_reporte_validacion.replace('var101', 'var' + str(var_id))
        sql = sql.replace('var_id = 101', 'var_id = ' + str(var_id))
        with connection.cursor() as cursor:
            cursor.execute(sql)




def generar_horario():
    print("Funciones generar Horario")
    file_horario_acum = open("scripts/plpgsql/generar_horario_acum.sql", 'r')
    sql_horario_acum = file_horario_acum.read()
    file_horario_prom = open("scripts/plpgsql/generar_horario_prom.sql", 'r')
    sql_horario_prom = file_horario_prom.read()

    for var_id in range(1, 23):
        sql1 = "SELECT es_acumulada FROM variable_variable WHERE var_id = %s;"
        with connection.cursor() as cursor:
            cursor.execute(sql1, (var_id,))
            es_acumulada = cursor.fetchone()
        try:
            es_acumulada = es_acumulada[0]
        except:
            continue

        var_id = str(var_id)
        if es_acumulada:
            sql_horario = sql_horario_acum
            sql_horario = sql_horario.replace('var1', 'var' + var_id)
            sql_horario = sql_horario.replace('f.var_id_id = 1', 'f.var_id_id = ' + var_id)
            sql_horario = sql_horario.replace('var_id = 1', 'var_id = ' + var_id)
        else:
            sql_horario = sql_horario_prom
            sql_horario = sql_horario.replace('var2', 'var' + var_id)
            sql_horario = sql_horario.replace('f.var_id_id = 2', 'f.var_id_id = ' + var_id)
            sql_horario = sql_horario.replace('var_id = 2', 'var_id = ' + var_id)

        with connection.cursor() as cursor:
            cursor.execute(sql_horario)


def generar_horario_profundidad():
    print("Funciones generar Horario profundidad")
    # file_horario_acum = open("scripts/plpgsql/generar_horario_acum_profundidad.sql", 'r')
    # sql_horario_acum = file_horario_acum.read()
    file_horario_prom = open("scripts/plpgsql/generar_horario_prom_profundidad.sql", 'r')
    sql_horario_prom = file_horario_prom.read()

    for var_id in range(101, 108):
        sql1 = "SELECT es_acumulada FROM variable_variable WHERE var_id = %s;"
        with connection.cursor() as cursor:
            cursor.execute(sql1, (var_id,))
            es_acumulada = cursor.fetchone()
        try:
            es_acumulada = es_acumulada[0]
        except:
            continue

        var_id = str(var_id)
        if es_acumulada:
            continue
            # sql_horario = sql_horario_acum.replace('var_id_id = 1', 'var_id_id = ' + var_id)
            # sql_horario = sql_horario.replace('var1', 'var' + var_id)
        else:
            sql_horario = sql_horario_prom.replace('101', str(var_id))

        with connection.cursor() as cursor:
            cursor.execute(sql_horario)



def generar_diario():
    print("Funciones Generar Diario")
    file_diario_acum = open("scripts/plpgsql/generar_diario_acum.sql", 'r')
    sql_diario_acum = file_diario_acum.read()
    file_diario_prom = open("scripts/plpgsql/generar_diario_prom.sql", 'r')
    sql_diario_prom = file_diario_prom.read()

    for var_id in range(1, 23):
        sql1 = "SELECT es_acumulada FROM variable_variable WHERE var_id = %s;"
        with connection.cursor() as cursor:
            cursor.execute(sql1, (var_id,))
            es_acumulada = cursor.fetchone()
        try:
            es_acumulada = es_acumulada[0]
        except:
            continue

        var_id = str(var_id)
        if es_acumulada:
            sql = sql_diario_acum.replace('var_id = 1', 'var_id = ' + var_id)
            sql = sql.replace('var1', 'var' + var_id)
        else:
            sql = sql_diario_prom.replace('var_id_id = 2', 'var_id_id = ' + var_id)
            sql = sql.replace('var2', 'var' + var_id)

        with connection.cursor() as cursor:
            cursor.execute(sql)



def generar_diario_profundidad():
    print("Funciones Generar Diario Profundidad")
    # file_diario_acum = open("scripts/plpgsql/generar_diario_acum.sql", 'r')
    # sql_diario_acum = file_diario_acum.read()
    file_diario_prom = open("scripts/plpgsql/generar_diario_prom_profundidad.sql", 'r')
    sql_diario_prom = file_diario_prom.read()

    for var_id in range(101, 108):
        sql1 = "SELECT es_acumulada FROM variable_variable WHERE var_id = %s;"
        with connection.cursor() as cursor:
            cursor.execute(sql1, (var_id,))
            es_acumulada = cursor.fetchone()
        try:
            es_acumulada = es_acumulada[0]
        except:
            continue

        var_id = str(var_id)
        if es_acumulada:
            continue
            # sql = sql_diario_acum.replace('var_id = 1', 'var_id = ' + var_id)
            # sql = sql.replace('var1', 'var' + var_id)
        else:
            sql_diario = sql_diario_prom.replace('101', str(var_id))

        with connection.cursor() as cursor:
            cursor.execute(sql_diario)



def generar_mensual():
    print("Generar Mensual")
    file_mensual_acum = open("scripts/plpgsql/generar_mensual_acum.sql", 'r')
    sql_mensual_acum = file_mensual_acum.read()
    file_mensual_prom = open("scripts/plpgsql/generar_mensual_prom.sql", 'r')
    sql_mensual_prom = file_mensual_prom.read()

    for var_id in range(1, 23):
        sql1 = "SELECT es_acumulada FROM variable_variable WHERE var_id = %s;"
        with connection.cursor() as cursor:
            cursor.execute(sql1, (var_id,))
            es_acumulada = cursor.fetchone()
        try:
            es_acumulada = es_acumulada[0]
        except:
            continue

        var_id = str(var_id)
        if es_acumulada:
            sql = sql_mensual_acum.replace('var_id = 1', 'var_id = ' + var_id)
            sql = sql.replace('var1', 'var' + var_id)
        else:
            sql = sql_mensual_prom.replace('var_id_id = 2', 'var_id_id = ' + var_id)
            sql = sql.replace('var2', 'var' + var_id)

        with connection.cursor() as cursor:
            cursor.execute(sql)



def generar_mensual_profundidad():
    print("Generar Mensual Profundidad")
    # file_mensual_acum = open("scripts/plpgsql/generar_mensual_acum.sql", 'r')
    # sql_mensual_acum = file_mensual_acum.read()
    file_mensual_prom = open("scripts/plpgsql/generar_mensual_prom_profundidad.sql", 'r')
    sql_mensual_prom = file_mensual_prom.read()

    for var_id in range(101, 108):
        sql1 = "SELECT es_acumulada FROM variable_variable WHERE var_id = %s;"
        with connection.cursor() as cursor:
            cursor.execute(sql1, (var_id,))
            es_acumulada = cursor.fetchone()
        try:
            es_acumulada = es_acumulada[0]
        except:
            continue

        var_id = str(var_id)
        if es_acumulada:
            continue
            # sql = sql_mensual_acum.replace('var_id = 1', 'var_id = ' + var_id)
            # sql = sql.replace('var1', 'var' + var_id)
        else:
            sql = sql_mensual_prom.replace('101', str(var_id))

        with connection.cursor() as cursor:
            cursor.execute(sql)


reporte_validacion()
reporte_validacion_profundidad()
inserccion_validacion()
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


