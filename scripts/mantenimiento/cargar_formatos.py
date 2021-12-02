import pandas as pd
from formato.models import Formato, Asociacion
from estacion.models import Estacion

def run():
    archivo_src='scripts/mantenimiento/formatos_de_carga.xlsx'
    df = pd.read_excel(archivo_src, header=0, skiprows=0, skipfooter=0, engine=None,
                        error_bad_lines=False, index_col=None)
    for index, row in df.iterrows():
        est_codigo = row['est_codigo']
        for_id = row['for_id']

        estacion = Estacion.objects.get(est_codigo=est_codigo)
        formato = Formato.objects.get(for_id=for_id)
        asociacion = Asociacion(for_id=formato, est_id=estacion)
        asociacion.save()
        print(" ---")
        print("Código: ", est_codigo)
        print("est_id: ", str(estacion.est_id))
        print("for_id: ", str(for_id))
