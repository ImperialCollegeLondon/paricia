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
from medicion.models import Medicion, CurvaDescarga
from formato.models import Clasificacion
from importacion.models import Importacion
from variable.models import Variable
from django.db.models import Prefetch
from cruce.models import Cruce
from validacion.models import Validacion

from medicion.forms import *
from medicion.functions import *
from home.functions import pagination


# Medicion views
class MedicionCreate(LoginRequiredMixin, CreateView):
    model = Medicion
    fields = ['var_id', 'est_id', 'med_fecha', 'med_valor', 'med_maximo',
              'med_minimo']

    def form_valid(self, form):
        return super(MedicionCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MedicionCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context


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
                self.lista = reporte_validacion(form)
                self.variable = form.cleaned_data['variable']
                self.estacion = form.cleaned_data['estacion']
                self.grafico = grafico2(self.lista, self.variable, self.estacion)
                self.inicio = form.cleaned_data['inicio']
                self.fin = form.cleaned_data['fin']
                return render(request, 'medicion/medicion_list.html',
                              {'lista': self.lista,
                               'variable': self.variable,
                               'estacion': self.estacion,
                               'grafico': self.grafico,
                               'inicio': self.inicio,
                               'fin': self.fin
                               })
        #return self.render_to_response(self.get_context_data(form=form))
        return HttpResponse('')


    def get_context_data(self, **kwargs):
        context = super(MedicionFilter, self).get_context_data(**kwargs)
        context['lista'] = self.lista
        context['variable'] = self.variable
        context['grafico'] = self.grafico
        return context

# Lista de datos crudos
class MedicionList(LoginRequiredMixin, FormView):
    template_name = 'medicion/medicion_list1.html'
    form_class = MedicionSearchForm
    success_url = '/medicion/'
    lista = []
    variable = ""

    def post(self, request, *args, **kwargs):
        form = MedicionSearchForm(self.request.POST or None)
        if form.is_valid():
            self.lista = filtrar(form)
            self.variable = form.cleaned_data['variable']
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(MedicionList, self).get_context_data(**kwargs)
        context['lista'] = self.lista
        context['variable'] = self.variable
        return context


# Clase para filtrar datos para la vista delete
class ListDelete(LoginRequiredMixin, FormView, ListView):
    template_name = 'medicion/list_delete.html'
    form_class = FilterDeleteForm
    success_url = '/medicion/listdelete/'
    model = Medicion
    variable = ""

    def post(self, request, *args, **kwargs):
        form = FilterDeleteForm(self.request.POST or None)
        if form.is_valid():
            self.lista = filtrar(form)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(ListDelete, self).get_context_data(**kwargs)
        context['lista'] = self.lista
        return context


# filtro para eliminar los datos
class FilterDelete(LoginRequiredMixin, FormView):
    template_name = 'medicion/filter_delete.html'
    form_class = FilterDeleteForm
    success_url = '/medicion/filterdelete/'
    # mensaje de confirmación
    mensaje = ""

    def post(self, request, *args, **kwargs):
        form = FilterDeleteForm(self.request.POST or None)
        if form.is_valid():
            eliminar(form)
            self.mensaje = "Datos Eliminados"
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(FilterDelete, self).get_context_data(**kwargs)
        context['mensaje'] = self.mensaje
        return context


class MedicionUpdate(LoginRequiredMixin, UpdateView):
    model = Medicion
    fields = ['med_valor', 'med_maximo', 'med_minimo']
    url = ""

    def get(self, request, *args, **kwargs):
        med_id = kwargs.get('pk')
        med_fecha = kwargs.get('fecha')
        var_id = kwargs.get('var_id')
        self.object = consultar_objeto(kwargs)
        self.url = "/medicion/" + med_id + "/" + med_fecha + "/" + var_id + "/"
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        modificar_medicion(kwargs, request.POST)
        self.object = consultar_objeto(kwargs)
        guardar_log(accion="Modificar", medicion=self.object, user=request.user)
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MedicionUpdate, self).get_context_data(**kwargs)
        context['url'] = self.url
        return context


class MedicionDelete(LoginRequiredMixin, UpdateView):
    model = Medicion
    fields = ['est_id', 'var_id', 'med_fecha', 'med_valor', 'med_valor', 'med_maximo', 'med_minimo']
    url = ""
    template_name = 'medicion/medicion_delete.html'

    def get(self, request, *args, **kwargs):
        med_id = kwargs.get('pk')
        med_fecha = kwargs.get('fecha')
        var_id = kwargs.get('var_id')
        self.object = consultar_objeto(kwargs)
        self.url = "/medicion/delete/" + med_id + "/" + med_fecha + "/" + var_id + "/"
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        eliminar_medicion(kwargs, request.POST)
        self.object = consultar_objeto(kwargs)
        guardar_log(accion="Eliminar", medicion=self.object, user=request.user)
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MedicionDelete, self).get_context_data(**kwargs)
        context['url'] = self.url
        return context


'''class MedicionImportacion(LoginRequiredMixin, FormView):
    model = Medicion
    template_name = 'medicion/medicion_importacion.html'
    form_class = MedicionSearchForm

    def get(self, request, *args, **kwargs):
        imp_id = kwargs.get('imp_id')
        importacion = Importacion.objects.get(imp_id=imp_id)
        clasificacion = Clasificacion.objects.filter(for_id=importacion.for_id)
        context = []
        for fila in clasificacion:
            data = {
                'estacion': importacion.est_id.est_id,
                'variable': fila.var_id.var_id,
                'inicio': importacion.imp_fecha_ini.strftime('%d/%m/%Y'),
                'fin': importacion.imp_fecha_fin.strftime('%d/%m/%Y')
            }
            form = MedicionSearchForm(data)
            if form.is_valid():
                # context[str(fila.var_id.var_codigo)]=consultar(form)
                consulta = consultar(form)
                obj_informacion = Informacion()
                obj_informacion.nombre = fila.var_id.var_nombre
                obj_informacion.lista = consulta
                obj_informacion.grafico = grafico(consulta, fila.var_id, importacion.est_id)
                context.append(obj_informacion)
            else:
                context = []
        return self.render_to_response(self.get_context_data(informacion=context, form=form))

    def get_context_data(self, **kwargs):
        context = super(MedicionImportacion, self).get_context_data(**kwargs)
        return context'''


class MedicionConsulta(LoginRequiredMixin,FormView):
    template_name = 'medicion/consulta.html'
    form_class = MedicionConsultaForm
    success_url = '/medicion/consulta'
    grafico = []

    def post(self, request, *args, **kwargs):
        form = MedicionConsultaForm(self.request.POST or None)
        if form.is_valid() and self.request.is_ajax():
            valores, maximos_abs, minimos_abs, tiempo = datos_instantaneos(form)
            self.grafico = grafico(form, valores, maximos_abs, minimos_abs, tiempo)
            return render(request, 'reportes/consultas/grafico.html',
                          {'grafico': self.grafico})
        # elif form.is_valid():
            # return self.export_excel(self.frecuencia, form)
        return render(request, 'home/form_error.html', {'form': form})


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

### proceso automatico de generacion de datos horarios diarios y mensuales
def generar_reportes_1variable(variable_id):
    threads[variable_id] = True
    cursor = connection.cursor()
    es_reporte_automatico = Variable.objects.filter(var_id=variable_id, reporte_automatico=True)
    if not es_reporte_automatico:
        del threads[variable_id]
        return
    variable = Variable.objects.filter(var_id=variable_id, reporte_automatico=True).values("var_modelo")
    variable = variable[0].get('var_modelo').lower()
    print(" ******************************** ")
    print(" ******************************** ")
    print("Estoy en medicion views ")
    print("Estoy en medicion views ")
    sql = "SELECT * FROM generar_horario_" + variable + "();"
    res = True
    while res:
        cursor.execute(sql)
        res = cursor.fetchone()[0]

    sql = "SELECT * FROM generar_diario_" + variable + "();"
    res = True
    while res:
        cursor.execute(sql)
        res = cursor.fetchone()[0]

    sql = "SELECT * FROM generar_mensual_" + variable + "();"
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
        varBusc = Variable.objects.get(var_id=variable_id)
        variable_nombre = varBusc.var_modelo.lower()
    except:
        estacion_id = None
        variable_id = None


    # Verificando datos json para evitar inyeccion SQL
    cambios_json = request.POST.get('cambios', None)

    #
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