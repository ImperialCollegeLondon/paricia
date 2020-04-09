# Este script permite cargar datos de un archivo excel a una tabla de la BD

import pandas as pd
from estacion.models import Estacion, SistemaCuenca

from telemetria.models import ConfigVisualizar
from variable.models import Variable
excel_file = '/Users/paulchicaiza/SynologyDrive/2020/SEDC/ConfigVisualizar.xlsx'
xl = pd.ExcelFile(excel_file)

variables = xl.parse('datos').set_index('id', drop=False).to_dict('index')

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
    #estacion = Estacion.objects.get(est_id=key)
    #sitemacuenca = SistemaCuenca.objects.get(id=row['nuevo_id'])
    print(row['estacion'], row['variable'])
    estacion = Estacion.objects.get(est_id=row['estacion'])
    variable = Variable.objects.get(var_id=row['variable'])
    obj_config_visualizar = ConfigVisualizar()
    obj_config_visualizar.estacion = estacion
    obj_config_visualizar.variable = variable
    obj_config_visualizar.umbral_superior = row['maximo']
    obj_config_visualizar.umbral_inferior = row['minimo']
    obj_config_visualizar.save()

    #estacion.sistemacuenca = sitemacuenca
    #estacion.save()
