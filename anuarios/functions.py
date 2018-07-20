# -*- coding: utf-8 -*-


from anuarios import models

from anuarios.formatoI import matrizI
from anuarios.formatoII import matrizII
from anuarios.formatoIII import matrizIII
from anuarios.formatoIV import matrizIV
from anuarios.formatoV import datos_viento, matrizV_mensual
from anuarios.formatoVI import matrizVI, datos_radiacion_maxima, datos_radiacion_minimo

from cruce.models import  Cruce


def calcular(form):
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
    estacion = form.cleaned_data['estacion']
    variable = form.cleaned_data['variable']
    periodo = form.cleaned_data['periodo']
    if variable.var_id in typeI:
        datos = matrizI(estacion, variable, periodo)
    elif variable.var_id in typeII:
        datos = matrizII(estacion, variable, periodo)
    elif variable.var_id in typeIII:
        datos = matrizIII(estacion, variable, periodo)
    elif variable.var_id in typeIV:
        datos = matrizIV(estacion, variable, periodo)
    elif variable.var_id in typeV:
        datos = matrizV_mensual(estacion, variable, periodo)
    elif variable.var_id in typeVI:
        datos = matrizVI(estacion, variable, periodo)
    return datos


def guardar_variable(datos, form):
    estacion = form.cleaned_data['estacion']
    variable = form.cleaned_data['variable']
    periodo = form.cleaned_data['periodo']
    if verficar_anuario(estacion, variable, periodo):
        borrar_datos(estacion, variable, periodo)
    if variable.var_id == 7:
        datos_radiacion_maxima(datos, estacion, periodo)
        datos_radiacion_minimo(datos, estacion, periodo)
    elif variable.var_id == 4 or variable.var_id == 5:
        viento = datos_viento(datos, estacion, periodo)
        for obj_viento in viento:
            obj_viento.save()
    else:
        for obj_variable in datos:
            obj_variable.save()


def borrar_datos(estacion, variable, periodo):
    if variable.var_id == 1:
        models.Precipitacion.objects.filter(est_id=estacion.est_id) \
            .filter(pre_periodo=periodo).delete()
    elif variable.var_id == 2:
        result = models.TemperaturaAire.objects.filter(est_id=estacion.est_id) \
            .filter(tai_periodo=periodo).delete()
    elif variable.var_id == 3:
        result = models.HumedadAire.objects.filter(est_id=estacion.est_id) \
            .filter(hai_periodo=periodo).delete()
    elif variable.var_id == 4 or variable.var_id == 5:
        result = models.Viento.objects.filter(est_id=estacion.est_id) \
            .filter(vie_periodo=periodo).delete()
    elif variable.var_id == 6:
        result = models.HumedadSuelo.objects.filter(est_id=estacion.est_id) \
            .filter(hsu_periodo=periodo).delete()
    elif variable.var_id == 7:
        result = models.RadiacionMaxima.objects.filter(est_id=estacion.est_id) \
            .filter(rad_periodo=periodo).delete()
        result = models.RadiacionMinima.objects.filter(est_id=estacion.est_id) \
            .filter(rad_periodo=periodo).delete()
    elif variable.var_id == 8:
        result = models.PresionAtmosferica.objects.filter(est_id=estacion.est_id) \
            .filter(pat_periodo=periodo).delete()
    elif variable.var_id == 9:
        result = models.TemperaturaAgua.objects.filter(est_id=estacion.est_id) \
            .filter(tag_periodo=periodo).delete()
    elif variable.var_id == 10:
        result = models.Caudal.objects.filter(est_id=estacion.est_id) \
            .filter(cau_periodo=periodo).delete()
    elif variable.var_id == 11:
        result = models.NivelAgua.objects.filter(est_id=estacion.est_id) \
            .filter(nag_periodo=periodo).delete()


def verficar_anuario(estacion, variable, periodo):
    result = False
    if variable.var_id == 1:
        result = models.Precipitacion.objects.filter(est_id=estacion.est_id) \
            .filter(pre_periodo=periodo).exists()
    elif variable.var_id == 2:
        result = models.TemperaturaAire.objects.filter(est_id=estacion.est_id) \
            .filter(tai_periodo=periodo).exists()
    elif variable.var_id == 3:
        result = models.HumedadAire.objects.filter(est_id=estacion.est_id) \
            .filter(hai_periodo=periodo).exists()
    elif variable.var_id == 4 or variable.var_id == 5:
        result = models.Viento.objects.filter(est_id=estacion.est_id) \
            .filter(vie_periodo=periodo).exists()
    elif variable.var_id == 6:
        result = models.HumedadSuelo.objects.filter(est_id=estacion.est_id) \
            .filter(hsu_periodo=periodo).exists()
    elif variable.var_id == 7:
        result = models.RadiacionMaxima.objects.filter(est_id=estacion.est_id) \
            .filter(rad_periodo=periodo).exists()
        result = models.RadiacionMinima.objects.filter(est_id=estacion.est_id) \
            .filter(rad_periodo=periodo).exists()
    elif variable.var_id == 8:
        result = models.PresionAtmosferica.objects.filter(est_id=estacion.est_id) \
            .filter(pat_periodo=periodo).exists()
    elif variable.var_id == 9:
        result = models.TemperaturaAgua.objects.filter(est_id=estacion.est_id) \
            .filter(tag_periodo=periodo).exists()
    elif variable.var_id == 10:
        result = models.Caudal.objects.filter(est_id=estacion.est_id) \
            .filter(cau_periodo=periodo).exists()
    elif variable.var_id == 11:
        result = models.NivelAgua.objects.filter(est_id=estacion.est_id) \
            .filter(nag_periodo=periodo).exists()
    return result


def template(variable):
    template = 'anuarios/tai.html'
    if variable.var_id == 1:
        template = 'anuarios/pre.html'
    elif variable.var_id == 2:
        template = 'anuarios/tai.html'
    elif variable.var_id == 3:
        template = 'anuarios/hai.html'
    elif variable.var_id == 4:
        template = 'anuarios/vvi.html'
    elif variable.var_id == 5:
        template = 'anuarios/dvi.html'
    elif variable.var_id == 6:
        template = 'anuarios/hsu.html'
    elif variable.var_id == 7:
        template = 'anuarios/rad.html'
    elif variable.var_id == 8:
        template = 'anuarios/pat.html'
    elif variable.var_id == 9:
        template = 'anuarios/tag.html'
    elif variable.var_id == 10:
        template = 'anuarios/cau.html'
    elif variable.var_id == 11:
        template = 'anuarios/nag.html'
    return template
def consultar_variables(estacion):
    cruce = list(Cruce.objects.filter(est_id=estacion))
    lista = {}
    for item in cruce:
        lista[item.var_id.var_id] = item.var_id.var_nombre
    return lista
