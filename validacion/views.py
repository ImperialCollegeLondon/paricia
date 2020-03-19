# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.views.generic import ListView, FormView

from validacion.forms import *
from medicion.forms import ValidacionSearchForm
from validacion import functions
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.http import JsonResponse,HttpResponse
from django.core.serializers.json import DjangoJSONEncoder


import json
from indices.views import DecimalEncoder

####para las vistas serializables de la api
#from .models import *
from .serializers import *
from rest_framework import generics
import re
import calendar


# Consular los periodos de validacion por estacion y variable
class PeriodosValidacion(LoginRequiredMixin, FormView):
    template_name = 'validacion/periodos_validacion.html'
    form_class = ValidacionSearchForm
    success_url = '/medicion/filter/'
    lista = []

    def post(self, request, *args, **kwargs):
        estacion_id = None
        variable_id = None
        try:
            estacion_id = int(request.POST.get('estacion', None))
            variable_id = int(request.POST.get('variable', None))
            variable = Variable.objects.get(var_id=variable_id)
            variable_id = variable.var_modelo.lower()
        except:
            pass

        intervalos = functions.periodos_validacion(est_id=estacion_id, var_id=variable_id)
        return render(request, self.template_name, {'intervalos': intervalos})


# Consulta de datos horarios crudos y/o validados por estacion, variable y hora
class DatosHorarios(LoginRequiredMixin, ListView):
    template_name = 'validacion/datos_horarios.html'

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            template = 'validacion/datos_horarios.html'
            est_id = kwargs.get('estacion')
            var_id = kwargs.get('variable')
            fecha_str = kwargs.get('fecha')
            datos = functions.consultar_horario(est_id, var_id, fecha_str)
            diccionario = {'datos': datos}
            return render(request, template, diccionario)
        return self.render_to_response(self.get_context_data(save=True))


# Consulta de datos diarios por reporte
class ValidacionDiaria(LoginRequiredMixin, FormView):
    template_name = 'validacion/validacion_diaria.html'
    form_class = ValidacionSearchForm
    success_url = '/validacion/diaria/'

    def post(self, request, *args, **kwargs):
        form = ValidacionSearchForm(self.request.POST or None)
        if form.is_valid():
            if self.request.is_ajax():
                variable = form.cleaned_data['variable']
                estacion = form.cleaned_data['estacion']
                inicio = form.cleaned_data['inicio']
                fin = form.cleaned_data['fin']

                lista = functions.reporte_diario(estacion, variable, inicio, fin)

                for fila in lista:
                    delattr(fila, '_state')
                    fila.dia = fila.dia.strftime("%Y-%m-%d")
                    fila.porcentaje = round(fila.porcentaje)

                # lista_nueva = [dict(fila.__dict__) for fila in lista if fila['state']]

                data = {'estacion': [{
                    'est_id': estacion.est_id,
                    'est_nombre': estacion.est_nombre,

                    }],
                    'variable': [{
                        'var_id': variable.var_id,
                        'var_nombre': variable.var_nombre,
                        'var_maximo': variable.var_maximo,
                        'var_minimo': variable.var_minimo,

                    }],
                    'datos': [dict(fila.__dict__) for fila in lista]
                }

                data_json = json.dumps(data, allow_nan=True, cls=DjangoJSONEncoder)

                #return JsonResponse(data, safe=False)
                return HttpResponse(data_json, content_type='application/json')

        # return self.render_to_response(self.get_context_data(form=form))
        return render(request, 'home/form_error.html', {'form': form})



class ValidacionBorrar(LoginRequiredMixin, FormView):
    template_name = 'validacion/borrar.html'
    form_class = BorrarForm
    success_url = '/validacion/borrar/'
    resultado = None

    def form_valid(self, form):
        estacion_id = form.cleaned_data['estacion'].est_id
        var_id = form.cleaned_data['variable'].var_id
        inicio = form.cleaned_data['inicio']
        fin = form.cleaned_data['fin']

        filas_validado = 0
        sql = "DELETE FROM validacion_var%%var_id%%validado WHERE estacion_id = %s AND fecha >= %s AND fecha <= %s;"
        sql = sql.replace('%%var_id%%', str(var_id))
        with connection.cursor() as cursor:
            cursor.execute(sql, [estacion_id, inicio, fin])
            filas_validado = cursor.rowcount

        filas_horario = 0
        sql = "DELETE FROM horario_var%%var_id%%horario WHERE estacion_id = %s AND fecha >= date_trunc('hour', %s) AND fecha <= date_trunc('hour', %s);"
        sql = sql.replace('%%var_id%%', str(var_id))
        with connection.cursor() as cursor:
            cursor.execute(sql, [estacion_id, inicio, fin])
            filas_horario = cursor.rowcount

        filas_diario = 0
        sql = "DELETE FROM diario_var%%var_id%%diario WHERE estacion_id = %s AND fecha >= date_trunc('day', %s) AND fecha <= date_trunc('day', %s);"
        sql = sql.replace('%%var_id%%', str(var_id))
        with connection.cursor() as cursor:
            cursor.execute(sql, [estacion_id, inicio, fin])
            filas_diario = cursor.rowcount

        filas_mensual = 0
        sql = "DELETE FROM mensual_var%%var_id%%mensual WHERE estacion_id = %s AND fecha >= date_trunc('month', %s) AND fecha <= date_trunc('month', %s);"
        sql = sql.replace('%%var_id%%', str(var_id))
        with connection.cursor() as cursor:
            cursor.execute(sql, [estacion_id, inicio, fin])
            filas_mensual = cursor.rowcount

        if self.request.is_ajax():
            data = {
                'filas_validado': filas_validado,
                'filas_horario': filas_horario,
                'filas_diario': filas_diario,
                'filas_mensual': filas_mensual
            }
            return JsonResponse(data)
        else:
            return super().form_valid(form)


# Vista para tadas las variables
class VarList(generics.ListAPIView):

    serializer_class = PrecipitacionSerial

    def get_queryset(self):
        ##### Truncar a un mes si la fecha fin es mas de unmes
        #####
        varibles = ["precipitacion", "temperatura_aire", "humedad_relativa", "velocidad_viento", "direcion_viento",
                    "humedad_suelo", "radiacion_solar", "presion_atmosferica", "temperatura_agua", "caudal",
                    "nivel_agua",
                    "voltaje_bateria", "caudal_aforo", "nivel_regleta", "direcion_rafaga", "recorrido_viento",
                    "gust_dir",
                    "gust_h", "gust_m", "temperatura_suelo", "radiacion_indirecta", "radiacion_suma"]
        varModel = ["Precipitacion", "temperatura_aire", "humedad_relativa", "velocidad_viento", "direcion_viento",
                    "humedad_suelo", "radiacion_solar", "presion_atmosferica", "temperatura_agua", "caudal",
                    "nivel_agua",
                    "voltaje_bateria", "caudal_aforo", "nivel_regleta", "direcion_rafaga", "recorrido_viento",
                    "gust_dir",
                    "gust_h", "gust_m", "temperatura_suelo", "radiacion_indirecta", "radiacion_suma"]
        varname = self.request.query_params.get('var', None)
        if varname in varibles:
            ind = varibles.index(varname)
            clasS = str(varModel[ind]) + "Serial"
            serializer_class = clasS
            tableD = globals()[str(varModel[ind])]
        print("class Serializer ", clasS)

        estacion_id = self.request.query_params.get('estacion_id', None)
        fecha = self.request.query_params.get('fecha', None)
        print(fecha)
        patron = re.compile(r'(\d{4})(-|/)(\d{1,2})(-|/)(\d{1,2})')
        regF = False
        if patron.match(fecha) is not None:
            fecha = fecha.replace('/', '-')
            fecha = fecha.split("-")
            day = calendar.monthrange(int(fecha[0]), int(fecha[1]))[1]
            fechaini = fecha[0] + '-' + fecha[1] +'-'+ fecha[2]
            if (int(fecha[2]) <= day):
                fechaFin = fecha[0] + '-' + fecha[1] + '-' + str(int(fecha[2]) + 1 )
            else:
                fechaFin = fecha[0] + '-' + fecha[1] + '-' + str(day)
            regF = True

        queryset = tableD.objects.all()[:5]
        if estacion_id is not None and regF == True:
            queryset = tableD.objects.filter(estacion_id=estacion_id, fecha__gte=fechaini, fecha__lte=fechaFin)[:]

        return queryset

    ### Vista para Var2Validado