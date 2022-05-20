import pandas as pd
from estacion.models import Estacion

from cruce.models import Cruce
from variable.models import Variable


def run():
    archivo_src = "scripts/mantenimiento/Estacion_Variable.xlsx"
    df = pd.read_excel(
        archivo_src,
        header=0,
        skiprows=0,
        skipfooter=0,
        engine=None,
        error_bad_lines=False,
        index_col=None,
    )
    for index, row in df.iterrows():
        est_id = row["est_id"]
        est_codigo = row["est_codigo"]
        var_id = row["var_id"]
        estacion = Estacion.objects.get(est_id=est_id)
        variable = Variable.objects.get(var_id=var_id)
        print(" ---")
        print("  Estación: ", estacion.est_codigo)
        print("  Variable: ", variable.var_nombre)

        cruce = Cruce(est_id=estacion, var_id=variable)
        cruce.save()
