from django.db import connection
from variable.models import Variable

def run():
    cursor = connection.cursor()
    variables = Variable.objects.filter(reporte_automatico=True)
    for variable in variables:
        print(variable)
        sql = "SELECT * FROM generar_mensual_" + str(variable.var_modelo).lower() + "();"
        res = True
        while res:
            cursor.execute(sql)
            res = cursor.fetchone()[0]

    print("cerrando la coneccion")
    cursor.close()