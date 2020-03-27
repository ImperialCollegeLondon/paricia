from django.db import connection
from variable.models import Variable

cursor = connection.cursor()
variables = Variable.objects.filter(reporte_automatico=True)
for variable in variables:
    #generar_anual_precipitacion
    sql = "SELECT * FROM generar_anual_" + str(variable.var_modelo).lower() + "();"
    res = True
    while res:
        cursor.execute(sql)
        res = cursor.fetchone()[0]