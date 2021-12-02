import pandas as pd
from estacion.models import Estacion
from variable.models import Variable
from frecuencia.models import Frecuencia

def run():
    archivo_src='scripts/mantenimiento/Frecuencia_Estacion_Variable.xlsx'
    df = pd.read_excel(archivo_src, header=0, skiprows=0, skipfooter=0, engine=None,
                        error_bad_lines=False, index_col=None)
    for index, row in df.iterrows():
        est_id = row['est_id']
        est_codigo = row['est_codigo']
        frecuencia = int(row['frecuencia'])
        var_id = row['var_id']
        fec_ini = row['fec_ini']
        estacion = Estacion.objects.get(est_id=est_id)
        variable = Variable.objects.get(var_id=var_id)
        print(" ---")
        print("  Estación: ", estacion.est_codigo)
        print("  Variable: ", variable.var_nombre)
        print("  Frecuencia: ", str(frecuencia))
        print("  Inicio: ", fec_ini)

        frecuencia = Frecuencia(
            est_id=estacion,
            var_id=variable,
            fre_valor=frecuencia,
            fre_fecha_ini=fec_ini)
        frecuencia.save()
