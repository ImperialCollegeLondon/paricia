from estacion.models import Tipo

tipo = (
    'Pluviométrica',
    'Climatológica',
    'Hidrológica',
)

for nombre in tipo:
    Tipo( tip_nombre=nombre ).save()
