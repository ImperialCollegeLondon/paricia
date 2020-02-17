# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from validacion.models import Validacion
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from validacion.forms import *
from medicion.forms import ValidacionSearchForm
from validacion import functions
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.http import JsonResponse
from variable.models import Variable

####para las vistas serializables de la api
#from .models import *
from .serializers import *
from rest_framework import generics
import re
import calendar


class ValidacionList(LoginRequiredMixin, ListView, FormView):
    model = Validacion
    paginate_by = 12
    template_name = 'validacion/validacion_list.html'
    form_class = ConsultaValidacionForm

    def post(self, request, *args, **kwargs):
        print("clase validacion list, metodo post")
        form = ConsultaValidacionForm(self.request.POST or None)
        page = kwargs.get('page')
        if form.is_valid() and self.request.is_ajax():
            self.object_list = form.filtrar(form)
        else:
            self.object_list = Validacion.objects.all()
        context = super(ValidacionList, self).get_context_data(**kwargs)
        #context.update(pagination(self.object_list, page, 12))
        return render(request, 'validacion/validacion_table.html', context)

    def get_context_data(self, **kwargs):
        context = super(ValidacionList, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        #context.update(pagination(self.object_list, page, 12))
        return context


class ValidacionDetail(LoginRequiredMixin, DetailView):
    model = Validacion

"""
class ValidacionUpdate(LoginRequiredMixin, UpdateView):
    model = Validacion
    fields = ['est_id', 'var_id', 'val_fecha', 'val_num_dat', 'val_fre_reg', 'val_porcentaje']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ValidacionUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class ValidacionDelete(LoginRequiredMixin, DeleteView):
    model = Validacion
    success_url = reverse_lazy('medicion:validacion_index')

"""


def procesar_validacion(request):
    print(" def procesar validación" )
    if request.method == 'POST':
        form = ValidacionProcess(request.POST)
        # if form.is_valid():
    else:
        form = ValidacionProcess()
    return render(request, 'validacion/validacion_procesar.html', {'form': form})


# lista de validaciones por estacion y variable
class ProcesarValidacion(LoginRequiredMixin, FormView):
    template_name = 'validacion/validacion_procesar.html'
    form_class = ValidacionProcess
    success_url = '/validacion/'

    def post(self, request, *args, **kwargs):
        form = ValidacionProcess(self.request.POST or None)
        if form.is_valid():
            # functions.guardar_validacion(form)
            datos = functions.generar_validacion(form)
            if self.request.is_ajax():
                return render(request, 'validacion/validacion_filtro.html', {'datos': datos})
            else:
                functions.guardar_validacion(datos)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(ProcesarValidacion, self).get_context_data(**kwargs)
        return context


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
            varBusc=Variable.objects.get(var_id=variable_id)
            variable_id = varBusc.var_modelo.lower()
        except:
            pass
        #intervalos = functions.periodos_validacion(est_id=estacion_id, var_id=variable_id)
        intervalos = functions.periodos_validacion(est_id=estacion_id, var_id=variable_id)
        return render(request, self.template_name, {'intervalos': intervalos})


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





### Vista para tadas las variables
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