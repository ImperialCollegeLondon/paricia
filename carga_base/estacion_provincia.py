from estacion.models import Provincia

provincia = (
    'Azuay',
    'Bolívar',
    'Cañar',
    'Carchi',
    'Chimborazo',
    'Cotopaxi',
    'Imbabura',
    'Loja',
    'Pichincha',
    'Tungurahua',
    'El Oro',
    'Esmeraldas',
    'Guayas',
    'Los Ríos',
    'Manabí',
    'Santo Domingo de los Tsáchilas',
    'Santa Elena',
    'Morona Santiago',
    'Napo',
    'Orellana',
    'Pastaza',
    'Sucumbíos',
    'Zamora Chinchipe',
    'Galápagos',
)

for nombre in provincia:
    Provincia( pro_nombre=nombre ).save()
