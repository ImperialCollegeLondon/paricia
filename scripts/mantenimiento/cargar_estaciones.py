import pandas as pd
from estacion.models import Estacion, Tipo, Pais, Region, Ecosistema, Socio, Sitio, SitioCuenca, Cuenca

def run():
    archivo_src='scripts/mantenimiento/Estaciones_iMHEA_SI.xlsx'
    df = pd.read_excel(archivo_src, header=0, skiprows=0, skipfooter=0, engine=None,
                        error_bad_lines=False, index_col=None)
    for index, row in df.iterrows():
        codigo = row['Código']
        print(" ---")
        print("Código: ", codigo)

        if not pd.isna(row['Descripción']):
            descripcion = row['Descripción']
        else:
            descripcion = None

        try:
            tipo = Tipo.objects.get(nombre=row['Tipo'])
        except:
            print("        No existe Tipo de estación: ", row['Tipo'])
            tipo = None

        try:
            pais = Pais.objects.get(nombre=row['País'])
        except:
            print("        No existe País: ", row['País'])
            pais = None

        try:
            region = Region.objects.get(nombre=row['Región'])
        except:
            print("        No existe Región: ", row['Región'])
            region = None

        try:
            ecosistema = Ecosistema.objects.get(nombre=row['Ecosistema'])
        except:
            print("        No existe Ecosistema: ", row['Ecosistema'])
            ecosistema = None

        try:
            socio = Socio.objects.get(nombre=row['Socio'])
        except:
            print("        No existe Socio: ", row['Socio'])
            socio = None

        try:
            sitio = Sitio.objects.get(nombre=row['Sitio'])
        except:
            print("        No existe Sitio: ", row['Sitio'])
            sitio = None

        try:
            cuenca = Cuenca.objects.get(nombre=row['Cuenca'])
        except:
            print("        No existe Cuenca: ", row['Cuenca'])
            cuenca = None


        try:
            sitiocuenca = SitioCuenca.objects.get(sitio=sitio, cuenca=cuenca)
        except:
            print("        No existe asociación Sitio-Cuenca: ", sitio, " - ", cuenca)
            sitiocuenca = None


        if not pd.isna(row['Latitud']):
            latitud = row['Latitud']
        else:
            print("        No existe Latitud:", row['Latitud'])
            latitud = None

        if not pd.isna(row['Longitud']):
            longitud = row['Longitud']
        else:
            print("        No existe Longitud: ", row['Longitud'])
            longitud = None

        if not pd.isna(row['Altura']):
            altura = row['Altura']
        else:
            print("        No existe Altura: ", row['Altura'])
            altura = None

        if not pd.isna(row['Estado']):
            estado = row['Estado']
            if estado == 'Operativa':
                estado = True
            elif estado == 'No operativa':
                estado = False
            else:
                print("        No existe Estado: ", row['Estado'])
                estado = None
        else:
            print("        No existe Estado: ", row['Estado'])
            estado = None

        estacion = Estacion(
            est_codigo=codigo,
            est_nombre=descripcion,
            tipo=tipo,
            pais=pais,
            region=region,
            ecosistema=ecosistema,
            socio=socio,
            sitiocuenca=sitiocuenca,
            est_estado=estado,
            est_latitud=latitud,
            est_longitud=longitud,
            est_altura=altura
        )
        estacion.save()
