from estacion.models import Tipo

tipo = (
    'Pluviométrica',
    'Meteorológica',
    'Hidrológica',
)

for nombre in tipo:
    Tipo( tip_nombre=nombre ).save()
