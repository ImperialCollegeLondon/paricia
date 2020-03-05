# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import time
from threading import Thread
import json
from medicion.models import CurvaDescarga
from formato.models import Clasificacion
from importacion.models import Importacion
from variable.models import Variable
from django.db.models import Prefetch
from cruce.models import Cruce
from validacion.models import Validacion

from medicion.forms import *
from medicion.functions import *
from home.functions import pagination


# filtro para la validación de Datos Crudos
class MedicionFilter(LoginRequiredMixin, FormView):
    template_name = 'medicion/medicion_filter.html'
    form_class = ValidacionSearchForm
    success_url = '/medicion/filter/'
    lista = []
    variable = ""
    grafico = None

    def post(self, request, *args, **kwargs):
        form = ValidacionSearchForm(self.request.POST or None)
        if form.is_valid():
            if self.request.is_ajax():
                variable = form.cleaned_data['variable']
                estacion = form.cleaned_data['estacion']
                inicio = form.cleaned_data['inicio']
                fin = form.cleaned_data['fin']
                self.grafico = grafico_validacion(variable, estacion, inicio, fin)

                return JsonResponse(self.grafico, safe=False)

        # return self.render_to_response(self.get_context_data(form=form))
        return render(request, 'home/form_error.html', {'form': form})

    def get_context_data(self, **kwargs):
        context = super(MedicionFilter, self).get_context_data(**kwargs)
        context['lista'] = self.lista
        context['variable'] = self.variable
        context['grafico'] = self.grafico
        return context


@login_required
def lista_datos_validacion(request):
    estacion_id = request.POST.get('estacion', None)
    variable_id = request.POST.get('variable', None)
    inicio = request.POST.get('inicio', None)
    fin = request.POST.get('fin', None)

    estacion = Estacion.objects.get(est_id=estacion_id)
    variable = Variable.objects.get(var_id=variable_id)
    inicio = datetime.datetime.strptime(inicio, '%d/%m/%Y')
    fin = datetime.datetime.strptime(fin, '%d/%m/%Y')
    lista = reporte_validacion(estacion, variable, inicio, fin)

    # lista = []
    # print("Fin datos validacion: ", datetime.datetime.now())
    return render(request, 'medicion/medicion_list.html',
                  {'lista': lista,
                   'variable': variable,
                   'estacion': estacion,
                   'inicio': inicio,
                   'fin': fin
                   })


class CurvaDescargaList(LoginRequiredMixin, ListView, FormView):
    # parámetros ListView
    model = CurvaDescarga
    paginate_by = 10
    # parámetros FormView
    template_name = 'medicion/curvadescarga_list.html'
    form_class = CurvaDescargaSearchForm

    def post(self, request, *args, **kwargs):
        form = CurvaDescargaSearchForm(self.request.POST or None)
        page = kwargs.get('page')
        if form.is_valid() and self.request.is_ajax:
            self.object_list = form.filtrar(form)
        else:
            self.object_list = CurvaDescarga.objects.all()
        context = super(CurvaDescargaList, self).get_context_data(**kwargs)
        context.update(pagination(self.object_list, page, 10))
        return render(request, 'medicion/curvadescarga_table.html', context)

    def get_context_data(self, **kwargs):
        context = super(CurvaDescargaList, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        context.update(pagination(self.object_list, page, 10))
        return context


class CurvaDescargaCreate(LoginRequiredMixin, CreateView):
    model = CurvaDescarga
    fields = ['estacion', 'fecha', 'funcion']

    def form_valid(self, form):
        return super(CurvaDescargaCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CurvaDescargaCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context


class CurvaDescargaDetail(LoginRequiredMixin, DetailView):
    model = CurvaDescarga


class CurvaDescargaUpdate(LoginRequiredMixin, UpdateView):
    model = CurvaDescarga
    fields = ['estacion', 'fecha', 'funcion']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CurvaDescargaUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class CurvaDescargaDelete(LoginRequiredMixin, DeleteView):
    model = CurvaDescarga
    success_url = reverse_lazy('medicion:curvadescarga_index')

threads = {}


def generar_reportes_1variable(variable_id):
    threads[variable_id] = True
    cursor = connection.cursor()
    es_reporte_automatico = Variable.objects.filter(var_id=variable_id, reporte_automatico=True)
    if not es_reporte_automatico:
        del threads[variable_id]
        return

    sql = "SELECT * FROM generar_horario_var" + str(variable_id) + "();"
    res = True
    while res:
        cursor.execute(sql)
        res = cursor.fetchone()[0]

    sql = "SELECT * FROM generar_diario_var" + str(variable_id) + "();"
    res = True
    while res:
        cursor.execute(sql)
        res = cursor.fetchone()[0]

    sql = "SELECT * FROM generar_mensual_var" + str(variable_id) + "();"
    res = True
    while res:
        cursor.execute(sql)
        res = cursor.fetchone()[0]

    del threads[variable_id]


###### usado para generar los datos diarios horarios y mensuales a partir de las validaciones
def stack_reportes(variable_id):
    while variable_id in threads:
        time.sleep(10)
    t = Thread(target=generar_reportes_1variable, args=(variable_id,))
    t.start()


@login_required
def variables(request):
    try:
        estacion_id = int(request.GET.get('estacion_id', None))
    except ValueError:
        estacion_id = None
    if estacion_id is not None:
        variables = Cruce.objects.prefetch_related(
            Prefetch('var_id', queryset=Variable.objects.all())
        ).filter(est_id=estacion_id)
    else:
        variables = Variable.objects.all()
    lista = {}
    for row in variables:
        lista[row.var_id.var_id] = row.var_id.var_nombre
    return JsonResponse(lista)


@login_required
def validacion_enviar(request):
    formato_fechahora = "%Y-%m-%d %H:%M:%S.u"
    formato_fecha = "%Y-%m-%d"

    try:
        estacion_id = int(request.POST.get('estacion_id', None))
        variable_id = int(request.POST.get('variable_id', None))
        variable = Variable.objects.get(var_id=variable_id)
        variable_nombre = variable.var_modelo.lower()
    except:
        estacion_id = None
        variable_id = None






    # Verificando datos json para evitar inyeccion SQL
    cambios_json = request.POST.get('cambios', None)

    cambios_lista = json.loads(cambios_json)
    fecha_inicio_dato = cambios_lista[0]['fecha']
    fecha_fin_dato = cambios_lista[-1]['fecha']
    # Borrar datos
    with connection.cursor() as cursor:
        sql = "DELETE FROM validacion_%%var_id%% WHERE estacion_id = %s AND fecha >= %s AND fecha <= %s;"
        sql = sql.replace('%%var_id%%', str(variable_nombre))
        print(sql)
        cursor.execute(sql, [estacion_id, fecha_inicio_dato, fecha_fin_dato])

    comentario = request.POST.get('comentario_general', None)

    resultado = False
    with connection.cursor() as cursor:
        cursor.callproc('insertar_' + variable_nombre + '_validacion', [estacion_id, cambios_json])
        resultado = cursor.fetchone()[0]
        ###############################################################################
        ###############################################################################
        #####usado para generar lso datos horario y diarios a partir de la validaciones
        ##t = Thread(target=stack_reportes, args=(variable_id,))
        ##t.start()
        ################
        ##############3
    if resultado:
        cambios_lista = json.loads(cambios_json)
        fecha_inicio_dato = cambios_lista[0]['fecha']
        fecha_fin_dato = cambios_lista[-1]['fecha']
        Validacion(
            var_id_id = variable_id,
            est_id_id = estacion_id,
            fecha_validacion = datetime.date.today(),
            fecha_inicio_datos = fecha_inicio_dato,
            fecha_fin_datos = fecha_fin_dato,
            comentario = comentario
        ).save()
        lista = {'resultado': resultado}
        return JsonResponse(lista)
    return None


class MedicionBorrar(LoginRequiredMixin, FormView):
    ### IMPORTANTE: SE BORRAN CRUDOS Y VALIDADOS
    template_name = 'medicion/borrar.html'
    form_class = BorrarForm
    success_url = '/medicion/borrar/'
    resultado = None

    def form_valid(self, form):
        estacion_id = form.cleaned_data['estacion'].est_id
        var_id = form.cleaned_data['variable'].var_id
        inicio = form.cleaned_data['inicio']
        fin = form.cleaned_data['fin']

        filas_crudo = 0
        sql = "DELETE FROM medicion_var%%var_id%%medicion WHERE estacion_id = %s AND fecha >= %s AND fecha <= %s;"
        sql = sql.replace('%%var_id%%', str(var_id))
        with connection.cursor() as cursor:
            cursor.execute(sql, [estacion_id, inicio, fin])
            filas_crudo = cursor.rowcount

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
                'filas_crudo': filas_crudo,
                'filas_validado': filas_validado,
                'filas_horario': filas_horario,
                'filas_diario': filas_diario,
                'filas_mensual': filas_mensual
            }
            return JsonResponse(data)
        else:
            return super().form_valid(form)
