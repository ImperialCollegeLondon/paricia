from sensor.models import Tipo

TIPO_NOMBRE = (
         'Termómetro',
         'Higrómetro',
         'Pluviógrafo',
         'Veleta',
         'Anemómetro',
         'Barómetro',
         'TDR',
         'Piranómetro',
         'Termómetro de agua',
         'Sensor de nivel'
    )
for nombre in TIPO_NOMBRE:
    Tipo(tip_nombre=nombre).save()
