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

from django.shortcuts import render
from anuarios import functions
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import  FormView
from anuarios.forms import AnuarioForm
#from anuarios.models import *
from validacion.models import *
import numpy as np
from django.db.models import Max, Min
# Create your views here.
import datetime

# lista de variables por estacion
def lista_variables(request, estacion):
    datos = functions.consultar_variables(estacion)
    return JsonResponse(datos)

    
class ProcesarVariables(LoginRequiredMixin, FormView):
    template_name = 'anuarios/procesar_variable.html'
    form_class = AnuarioForm
    success_url = '/anuarios/procesar'

    def post(self, request, *args, **kwargs):
        form = AnuarioForm(self.request.POST or None)
        save = False
        if form.is_valid() and self.request.is_ajax():
            datos = functions.calcular(form)
            template = functions.template(form.cleaned_data['variable'])
            exists = functions.verficar_anuario(form.cleaned_data['estacion']
                                                , form.cleaned_data['variable'], form.cleaned_data['periodo'])
            functions.guardar_variable(datos, form)
            return render(request, template, {'datos': datos, 'exists': exists})

        return self.render_to_response(self.get_context_data(form=form, save=True))

    def get_context_data(self, **kwargs):
        context = super(ProcesarVariables, self).get_context_data(**kwargs)
        return context

def listar_anio(request, estacion):
    #modelo = 'Var'+'Anuario'
    #modelo = globals()[modelo]
    now = datetime.datetime.now()
    validados = Var1Validado.objects.filter(estacion_id__exact=estacion).aggregate(Max('fecha'), Min('fecha'))
    validados1 = Var2Validado.objects.filter(estacion_id__exact=estacion).aggregate(Max('fecha'), Min('fecha'))
    validados2 = Var3Validado.objects.filter(estacion_id__exact=estacion).aggregate(Max('fecha'), Min('fecha'))
    validados3 = Var6Validado.objects.filter(estacion_id__exact=estacion).aggregate(Max('fecha'), Min('fecha'))
    validados4 = Var7Validado.objects.filter(estacion_id__exact=estacion).aggregate(Max('fecha'), Min('fecha'))
    validados5 = Var8Validado.objects.filter(estacion_id__exact=estacion).aggregate(Max('fecha'), Min('fecha'))
    validados6 = Var9Validado.objects.filter(estacion_id__exact=estacion).aggregate(Max('fecha'), Min('fecha'))
    validados7 = Var10Validado.objects.filter(estacion_id__exact=estacion).aggregate(Max('fecha'), Min('fecha'))
    validados8 = Var11Validado.objects.filter(estacion_id__exact=estacion).aggregate(Max('fecha'), Min('fecha'))
    validados9 = Viento.objects.filter(estacion_id__exact=estacion).aggregate(Max('fecha'), Min('fecha'))
    mini = [validados['fecha__min'], validados1['fecha__min'], validados2['fecha__min'], validados3['fecha__min'],
             validados4['fecha__min'], validados5['fecha__min'], validados6['fecha__min'], validados7['fecha__min'],
             validados8['fecha__min'], validados9['fecha__min']]
    maxi = [validados['fecha__max'], validados1['fecha__max'], validados2['fecha__max'], validados3['fecha__max'],
             validados4['fecha__max'], validados5['fecha__max'], validados6['fecha__max'], validados7['fecha__max'],
             validados8['fecha__max'], validados9['fecha__max']]
    
    mini = [i for i in mini if i] 
    maxi = [i for i in maxi if i] 
    if maxi != None and mini != None and mini != [] and maxi != [] :
        fechas = list(range( (np.min(mini)).year, now.year+1))
    else:
        fechas = ["No existen datos"]
    return JsonResponse(fechas, safe=False)