import fnmatch
import os

directorio_base = "/home/program/Downloads/imhea2"


def dividir_archivo(ruta, nombre_archivo):
    ruta_completa_archivo = os.path.join(ruta, nombre_archivo)
    with open(ruta_completa_archivo, "r") as infile:
        ruta_completa_SIN_EXTENSION = ruta_completa_archivo.split(".")[0]
        cabecera = infile.readline()
        part = 1
        eof = False
        while eof == False:
            with open(
                ruta_completa_SIN_EXTENSION + "_part" + str(part).zfill(2) + ".csv", "w"
            ) as outfile:
                outfile.write(cabecera)
                eopart = False
                while eopart == False:
                    line = infile.readline()
                    outfile.write(line)
                    if any(x in line for x in ["v", "V"]):
                        part = part + 1
                        eopart = True
                    elif not line:
                        eopart = True
                        eof = True
            outfile.close()
    infile.close()


def run():
    for (ruta, directorios, archivos) in os.walk(directorio_base):
        print("Ruta: ", str(ruta))
        for nombre_archivo in sorted(archivos):
            if fnmatch.fnmatch(nombre_archivo, "*.[cC][sS][vV]"):
                print("    Archivo: ", str(nombre_archivo))
                dividir_archivo(ruta, nombre_archivo)
