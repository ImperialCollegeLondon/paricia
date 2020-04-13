# Este script crea las funciones necesarias para el modulo validacion.
# creacion de las funcion para mostrar los datos para validar
from django.db import connection


variables = ["precipitacion", "temperaturaaire", "humedadaire", "velocidadviento", "direccionviento", "humedadsuelo",
             "radiacionsolar", "presionatmosferica", "temperaturaagua", "caudal", "nivelagua"]


def aplicar_validacion_diaria():
    cursor = connection.cursor()
    print("Funcion de validacion diaria")

    file_validacion_acumulada = open("scripts/plpgsql/validacion_diaria_acu.sql", 'r')
    file_validacion_promedio = open("scripts/plpgsql/validacion_diaria_prom.sql", 'r')

    print(file_validacion_promedio)

    sql_validacion_acumulada = file_validacion_acumulada.read()
    sql_validacion_promedio = file_validacion_promedio.read()

    for index, var in enumerate(variables):
        print("Variable ", var, "indice ", index + 1)
        if index == 0:
            cursor.execute(sql_validacion_acumulada)
        else:
            sql_validacion_promedio = sql_validacion_promedio.replace('modelo', var)
            sql_validacion_promedio = sql_validacion_promedio.replace('__var_id__', str(index + 1))
            cursor.execute(sql_validacion_promedio)

    cursor.close()


aplicar_validacion_diaria()
