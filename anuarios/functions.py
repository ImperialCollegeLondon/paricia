################################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos (iMHEA)
# basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#         Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS), Ecuador.
#         Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones creadoras,
#              ya sea en uso total o parcial del código.

from cruce.models import Cruce
from anuarios import models

from anuarios.formatoI import matrizI
from anuarios.formatoII import get_precipitacion
from anuarios.formatoIII import matrizIII
from anuarios.formatoIV import matrizIV
from anuarios.formatoV import datos_viento, matrizV_mensual
from anuarios.formatoVI import matrizVI, datos_radiacion_maxima, datos_radiacion_minimo


def consultar_variables(estacion):
    cruce = list(Cruce.objects.filter(est_id=estacion).exclude(var_id=10))
    lista = {}
    for item in cruce:
        lista[item.var_id.var_id] = item.var_id.var_nombre
    return lista

#def calcular(form):
def calcular(estacion,variable,periodo,):
    print('calcular')
    datos = []
    valid = False
    # humedadsuelo,presionatmosferica,temperaturaagua,caudal,nivelagua
    typeI = [6, 8, 9, 10, 11]
    # precipitacion
    typeII = [1]
    # temperaturaaire
    typeIII = [2]
    # humedadaire
    typeIV = [3]
    # direccion y velocidad
    typeV = [4, 5]
    # radiacion
    typeVI = [7]
    estacion = estacion
    variable = variable
    periodo = periodo
    tipo = 'validado'

    if variable in typeI:
        datos = matrizI(estacion, variable, periodo, tipo)
    elif variable in typeII:
        datos = get_precipitacion(estacion, variable, periodo, tipo)
    elif variable in typeIII:
        datos = matrizIII(estacion, variable, periodo, tipo)
    elif variable in typeIV:
        datos = matrizIV(estacion, variable, periodo, tipo)
    elif variable in typeV:
        datos = matrizV_mensual(estacion, variable, periodo, tipo)
    elif variable in typeVI:
        datos = matrizVI(estacion, variable, periodo, tipo)
    return datos

def template(variable):
    print('template')
    template = ''
    if variable == 1:
        template = 'anuarios/pre.html'
    elif variable == 2:
        template = 'anuarios/tai.html'
    elif variable == 3:
        template = 'anuarios/hai.html'
    elif variable == 4:
        template = 'anuarios/vvi.html'
    elif variable == 5:
        template = 'anuarios/dvi.html'
    elif variable == 6:
        template = 'anuarios/hsu.html'
    elif variable == 7:
        template = 'anuarios/rad.html'
    elif variable == 8:
        template = 'anuarios/pat.html'
    elif variable == 9:
        template = 'anuarios/tag.html'
    elif variable == 10:
        template = 'anuarios/cau.html'
    elif variable == 11:
        template = 'anuarios/nag.html'
    return template



def verficar_anuario(estacion, variable, periodo):
    print(verficar_anuario)
    result = False
    if variable == 1:
        result = models.Var1Anuarios.objects.filter(est_id=estacion.est_id) \
            .filter(pre_periodo=periodo).exists()
    elif variable == 2:
        result = models.Var2Anuarios.objects.filter(est_id=estacion.est_id) \
            .filter(tai_periodo=periodo).exists()
    elif variable == 3:
        result = models.Var3Anuarios.objects.filter(est_id=estacion.est_id) \
            .filter(hai_periodo=periodo).exists()
    elif variable == 4 or variable == 5:
        result = models.Viento.objects.filter(est_id=estacion.est_id) \
            .filter(vie_periodo=periodo).exists()
    elif variable == 6:
        result = models.Var6Anuarios.objects.filter(est_id=estacion.est_id) \
            .filter(hsu_periodo=periodo).exists()
    elif variable == 7:
        result = models.RadiacionMaxima.objects.filter(est_id=estacion.est_id) \
            .filter(rad_periodo=periodo).exists()
        result = models.RadiacionMinima.objects.filter(est_id=estacion.est_id) \
            .filter(rad_periodo=periodo).exists()
    elif variable == 8:
        result = models.Var8Anuarios.objects.filter(est_id=estacion.est_id) \
            .filter(pat_periodo=periodo).exists()
    elif variable == 9:
        result = models.Var9Anuarios.objects.filter(est_id=estacion.est_id) \
            .filter(tag_periodo=periodo).exists()
    elif variable == 10:
        result = models.Var10Anuarios.objects.filter(est_id=estacion.est_id) \
            .filter(cau_periodo=periodo).exists()
    elif variable == 11:
        result = models.Var11Anuarios.objects.filter(est_id=estacion.est_id) \
            .filter(nag_periodo=periodo).exists()
    return result

def guardar_variable(datos, estacion, variable, periodo):
    #estacion = form.cleaned_data['estacion']
    #variable = form.cleaned_data['variable']
    #periodo = form.cleaned_data['periodo']
    print('guardar_variable')
    if verficar_anuario(estacion, variable, periodo):
        borrar_datos(estacion, variable, periodo)
    if variable == 7:
        datos_radiacion_maxima(datos, estacion, periodo)
        datos_radiacion_minimo(datos, estacion, periodo)
    elif variable == 4 or variable == 5:
        viento = datos_viento(datos, estacion, periodo)
        for obj_viento in viento:
            obj_viento.save()
    else:
        for obj_variable in datos:
            obj_variable.save()

def borrar_datos(estacion, variable, periodo):
    if variable == 1:
        models.Var1Anuarios.objects.filter(est_id=estacion.est_id) \
            .filter(pre_periodo=periodo).delete()
    elif variable == 2:
        models.Var2Anuarios.objects.filter(est_id=estacion.est_id) \
            .filter(tai_periodo=periodo).delete()
    elif variable == 3:
        models.Var3Anuarios.objects.filter(est_id=estacion.est_id) \
            .filter(hai_periodo=periodo).delete()
    elif variable == 4 or variable == 5:
        models.Viento.objects.filter(est_id=estacion.est_id) \
            .filter(vie_periodo=periodo).delete()
    elif variable == 6:
        models.Var6Anuarios.objects.filter(est_id=estacion.est_id) \
            .filter(hsu_periodo=periodo).delete()
    elif variable == 7:
        models.RadiacionMaxima.objects.filter(est_id=estacion.est_id) \
            .filter(rad_periodo=periodo).delete()
        models.RadiacionMinima.objects.filter(est_id=estacion.est_id) \
            .filter(rad_periodo=periodo).delete()
    elif variable == 8:
        models.Var8Anuarios.objects.filter(est_id=estacion.est_id) \
            .filter(pat_periodo=periodo).delete()
    elif variable == 9:
        models.Var9Anuarios.objects.filter(est_id=estacion.est_id) \
            .filter(tag_periodo=periodo).delete()
    elif variable == 10:
        models.Var10Anuarios.objects.filter(est_id=estacion.est_id) \
            .filter(cau_periodo=periodo).delete()
    elif variable == 11:
        models.Var11Anuarios.objects.filter(est_id=estacion.est_id) \
            .filter(nag_periodo=periodo).delete()
