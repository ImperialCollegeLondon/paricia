
from datetime import datetime

from django.views import generic
from indices.forms import *
from .functions import getVarValidado, acumularDoble, intensidadDiracion, getCaudalFrec, IndicaPreci, IndicaCaudal
from django.shortcuts import render
# Create your views here.
from django.http import JsonResponse, HttpResponse
from anuarios.models import *
import json
import decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return {'__Decimal__': str(obj)}
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

class Doblemasa(generic.FormView):
    template_name = "indices/doblemasa.html"
    form_class = SearchForm
    success_url = "indices/doblemasa"
    def post(self, request, *args, **kwargs):
        form = SearchForm(self.request.POST or None)
        #try:
        estacion1_id = int(request.POST.get('estacion1', None))
        estacion2_id = int(request.POST.get('estacion2', None))
        frecuencia = int(request.POST.get('frecuencia',None))
        variable_id = 1
        tinicio = request.POST.get('inicio', None)
        tfin = request.POST.get('fin', None)
        #print("tinico ",tinicio,"tfin ",tfin, " <=> frecuencia : ",frecuencia)
        inicio = datetime.strptime(tinicio+" 00:00:00", '%d/%m/%Y %H:%M:%S')
        fin = datetime.strptime(tfin+" 23:59:00", '%d/%m/%Y %H:%M:%S')
        intervalos = getVarValidado(variable_id,estacion1_id, inicio,fin, frecuencia)
        intervalos1 = getVarValidado(variable_id, estacion2_id, inicio, fin, frecuencia)
        data = json.dumps(acumularDoble(intervalos,intervalos1,frecuencia),allow_nan=True,cls=DecimalEncoder)
        #print(data)
        #intervalosSerial = serializers.serialize('json',intervalos, fields=('id','fecha','valor') )
        return HttpResponse(data, content_type='application/json')
        #return HttpResponse(intervalosSerial, content_type='application/json')

class IndPrecip(generic.FormView):
    """Calcula los indices de precipitacion dispinibles para la estación selecionada"""
    template_name = "indices/precipitacion.html"
    form_class = IndPrecipForm
    success_url = "indices/precipitacion.html"
    def post(self, request, *args, **kwargs):
        form = SelecEstForm(self.request.POST or None)
        # try:
        estacion_id = int(request.POST.get('estacion', None))
        #anualizar(estacion_id)
        data = IndicaPreci(estacion_id)
        data = json.dumps(data, allow_nan=True, cls=DecimalEncoder)
        return HttpResponse(data, content_type='application/json')

class IndCaudal(generic.FormView):
    """Calcula los indices de caudal dispinibles para la estación selecionada"""
    template_name = "indices/caudal.html"
    form_class = IndCaudForm
    success_url = "indices/caudal.html"
    def post(self, request, *args, **kwargs):
        form = SelecEstForm(self.request.POST or None)
        # try:
        estacion_id = int(request.POST.get('estacion', None))
        #anualizar(estacion_id)
        data = IndicaCaudal(estacion_id)
        data = json.dumps(data, allow_nan=True, cls=DecimalEncoder)
        return HttpResponse(data, content_type='application/json')


class IntensidadRR(generic.FormView):
    """Raliza la grafica para una estacion de la intensidad vs la duracion"""
    template_name = "indices/intendura.html"
    form_class = SelecEstForm
    success_url = "indices/intendura.html"

    def post(self, request, *args, **kwargs):
        estacion_id = int(request.POST.get('estacion', None))
        print("Estacion a buscar " , estacion_id)
        tinicio = request.POST.get('inicio', None)
        tfin = request.POST.get('fin', None)
        inicio = datetime.strptime(tinicio + " 00:00:00", '%d/%m/%Y %H:%M:%S')
        fin = datetime.strptime(tfin + " 23:59:00", '%d/%m/%Y %H:%M:%S')
        data = intensidadDiracion(estacion_id,inicio,fin)
        data = json.dumps(data, allow_nan=True, cls=DecimalEncoder)
        return HttpResponse(data, content_type='application/json')

class DuracionCaudal(generic.FormView):
    #duracioncaudal.html
    """Raliza la grafica para una estacion de la duracion del caudal"""
    template_name = "indices/duracioncaudal.html"
    form_class = SelecCaudalForm
    success_url = "indices/duracioncaudal.html"
    def post(self, request, *args, **kwargs):
        estacion_id = int(request.POST.get('estacion', None))
        tinicio = request.POST.get('inicio', None)
        tfin = request.POST.get('fin', None)
        frecuencia = int(request.POST.get('frecuencia', None))
        inicio = datetime.strptime(tinicio + " 00:00:00", '%d/%m/%Y %H:%M:%S')
        fin = datetime.strptime(tfin + " 23:59:00", '%d/%m/%Y %H:%M:%S')
        data = getCaudalFrec(estacion_id,inicio,fin,frecuencia)
        print(data)
        #data = {"mensaje":"hola mundo "}
        #data = json.dumps(data, allow_nan=True, cls=DecimalEncoder)
        return HttpResponse(data, content_type='application/json')