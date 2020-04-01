from django.db import connection
from variable.models import Variable

def run():
    cursor = connection.cursor()
    variables = Variable.objects.filter(reporte_automatico=True).filter(var_id=11)
    for variable in variables:
        print(variable.var_modelo)
        sql = "SELECT * FROM generar_horario_" + str(variable.var_modelo).lower() + "();"
        res = True
        while res:
            cursor.execute(sql)
            res = cursor.fetchone()[0]

