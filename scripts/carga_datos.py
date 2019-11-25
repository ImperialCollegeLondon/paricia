import pandas as pd
from estacion.models import Estacion, SistemaCuenca
from variable.models import Parametro
excel_file = '/media/sf_compartida/estaciones_Sistemas_Cuenca.xlsx'
xl = pd.ExcelFile(excel_file)
#estaciones = xl.parse('estaciones').set_index('id', drop=False).to_dict('index')
variables = xl.parse('estaciones').set_index('id', drop=False).to_dict('index')

'''for key, row in estaciones.items():
    # print(key, row)
    _row = dict(
        identificador=row['identificador'],
        codigo=row['codigo'],
        nombre=row['nombre'],
        transmision=row['transmision'],
        latitud=row['latitud'],
        longitud=row['longitud'],
        provincia=row['provincia'],
        canton=row['canton'],
        parroquia=row['parroquia'],
        categoria=row['tipo']
    )
    print(_row)

    Inamhi(**_row).save()'''
'''
for key,row in variables.items():
    
    _row = dict(
        parametro=row['parametro'],
        nombre=row['nombre'],
        estadistico=row['estadistico'],
        unidad=row['unidad'],
        trasmision=row['transmision']
    )
    Parametro(**_row).save()
'''

for key, row in variables.items():
    estacion = Estacion.objects.get(est_id=key)
    sitemacuenca = SistemaCuenca.objects.get(id=row['nuevo_id'])

    estacion.sistemacuenca = sitemacuenca
    estacion.save()
