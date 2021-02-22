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

from django.db import connection

#2 temperaturaambiente; 3 humedadrelativa, temperaturaaire,humedadaire

variables = ["precipitacion", "temperaturaambiente", "humedadrelativa", "velocidadviento", "direccionviento", "humedadsuelo",
             "radiacionsolar", "presionatmosferica", "temperaturaagua", "caudal", "nivelagua", "voltajebateria", "caudalaforo",
             "nivelregleta","direccionvientorafaga","recorridoviento","gustdir","gusth","gustm","temperaturasuelo","radiacionsolarsuma",]

def aplicar_validacion_diaria():
    cursor = connection.cursor()
    print("Funcion de validacion diaria")

    file_validacion_acumulada = open("scripts/plpgsql/validacion_diaria_acu.sql", 'r')
    file_validacion_promedio = open("scripts/plpgsql/validacion_diaria_prom.sql", 'r')
    file_validacion_viento = open("scripts/plpgsql/validacion_diaria_viento.sql", 'r')
    file_validacion_agua = open("scripts/plpgsql/validacion_diaria_agua.sql", 'r')

    sql_validacion_acumulada = file_validacion_acumulada.read()
    sql_validacion_promedio = file_validacion_promedio.read()
    sql_validacion_viento = file_validacion_viento.read()
    sql_validacion_agua = file_validacion_agua.read()

    for index, var in enumerate(variables):
        print("Variable ", var, "indice ", index + 1)
        if index == 0:
            cursor.execute(sql_validacion_acumulada)
        elif index == 3:
            print("Viento")
            cursor.execute(sql_validacion_viento)
        elif index == 4:
            pass
        elif index == 9:
            print("Caudal")
            cursor.execute(sql_validacion_agua)
        #elif index == 10:
        #    pass
        else:
            funcion_sql = sql_validacion_promedio.replace('modelo', var)
            funcion_sql = funcion_sql.replace('%%variable%%','var'+str(index + 1))
            funcion_sql = funcion_sql.replace('%%var_id%%', str(index + 1))
            cursor.execute(funcion_sql)

    cursor.close()


def aplicar_validacion_cruda():
    cursor = connection.cursor()
    print("Funcion Validacion Cruda")

    file_validacion_acumulada = open("scripts/plpgsql/validacion_crudos_acu.sql", 'r')
    file_validacion_promedio = open("scripts/plpgsql/validacion_crudos_prom.sql", 'r')
    file_validacion_viento = open("scripts/plpgsql/validacion_crudos_viento.sql", 'r')
    file_validacion_agua = open("scripts/plpgsql/validacion_crudos_agua.sql", 'r')

    sql_validacion_acumulada = file_validacion_acumulada.read()
    sql_validacion_promedio = file_validacion_promedio.read()
    sql_validacion_viento = file_validacion_viento.read()
    sql_validacion_agua = file_validacion_agua.read()

    for index, var in enumerate(variables):
        print("Variable ", var, "indice ", index + 1)
        if index == 0:
            cursor.execute(sql_validacion_acumulada)
        elif index == 3:
            print("Viento")
            cursor.execute(sql_validacion_viento)
        elif index == 4:
            pass
        elif index == 9:
            print("Caudal")
            cursor.execute(sql_validacion_agua)
        #elif index == 10:
        #    pass
        else:
            funcion_sql = sql_validacion_promedio.replace('%%modelo%%',var)
            funcion_sql = funcion_sql.replace('%%variable%%','var'+str(index + 1))
            funcion_sql = funcion_sql.replace('%%var_id%%', str(index + 1))
            cursor.execute(funcion_sql)

    
    cursor.close()


# Reporte de Datos Crudos que aun no estan validados
def aplicar_reporte_crudos():
    cursor = connection.cursor()
    print("Funcion Reporte Crudos")

    file_reporte_acumulada = open("scripts/plpgsql/reporte_crudos_acu.sql", 'r')
    file_reporte_promedio = open("scripts/plpgsql/reporte_crudos_prom.sql", 'r')
    file_reporte_viento = open("scripts/plpgsql/reporte_crudos_viento.sql", 'r')
    file_reporte_agua = open("scripts/plpgsql/reporte_crudos_agua.sql", 'r')

    sql_reporte_acumulada = file_reporte_acumulada.read()
    sql_reporte_promedio = file_reporte_promedio.read()
    sql_reporte_viento = file_reporte_viento.read()
    sql_reporte_agua = file_reporte_agua.read()

    for index, var in enumerate(variables):
        print("Variable ", var, "indice ", index + 1)
        if index == 0:
            cursor.execute(sql_reporte_acumulada)
        elif index == 3:
            cursor.execute(sql_reporte_viento)
        elif index == 4:
            pass
        elif index == 9:
            cursor.execute(sql_reporte_agua)
        #elif index == 10:
        #    pass
        else:
            funcion_sql = sql_reporte_promedio.replace('%%modelo%%', var).replace('%%var_id%%',str(index + 1))
            funcion_sql = funcion_sql.replace('%%variable%%','var'+str(index + 1))
            cursor.execute(funcion_sql)

    cursor.close()


def aplicar_insert_crudos():
    cursor = connection.cursor()
    print("Funcion Insertar Datos Crudos")

    file_validacion_acumulada = open("scripts/plpgsql/insertar_validacion_acu.sql", 'r')
    file_validacion_promedio = open("scripts/plpgsql/insertar_validacion_pro.sql", 'r')
    file_validacion_viento = open("scripts/plpgsql/insertar_validacion_viento.sql", 'r')
    file_validacion_agua = open("scripts/plpgsql/insertar_validacion_agua.sql", 'r')

    sql_validacion_acumulada = file_validacion_acumulada.read()
    sql_validacion_promedio = file_validacion_promedio.read()
    sql_validacion_viento = file_validacion_viento.read()
    sql_validacion_agua = file_validacion_agua.read()

    for index, var in enumerate(variables):
        print("Variable ", var, "indice ", index + 1)
        if index == 0:
             cursor.execute(sql_validacion_acumulada)
        elif index == 3:
            print("**********-*")
            print(sql_validacion_viento)
            print("**********-*")
            cursor.execute(sql_validacion_viento)
        elif index == 4:
            pass
        #elif index == 10:
        #    cursor.execute(sql_validacion_agua)
        #elif index == 11:
        #    pass
        else:
            funcion_sql = sql_validacion_promedio.replace('%%modelo%%', var).replace('%%var_id%%', str(index + 1))
            cursor.execute(funcion_sql)
    cursor.close()


def cargar_type():
    cursor = connection.cursor()
    print("Insertar types")
    sqla = open("scripts/plpgsql/type_data.sql", 'r')
    cursor.execute(sqla.read())
    cursor.close()

cargar_type()
aplicar_validacion_cruda()
####3
aplicar_validacion_diaria()
aplicar_insert_crudos()
aplicar_reporte_crudos()
