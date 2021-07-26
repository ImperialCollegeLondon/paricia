# -*- coding: utf-8 -*-

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

from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.urls import reverse_lazy

from validacion.forms import *
from validacion.models import Validacion
from validacion.functions import *
from variable.models import Variable

import time
from threading import Thread
import json
import datetime


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



def stack_reportes(variable_id):
    while variable_id in threads:
        time.sleep(10)
    t = Thread(target=generar_reportes_1variable, args=(variable_id,))
    t.start()


@permission_required('validacion.hidro_o_calidad_enviar_validacion')
def validacion_enviar(request):
    formato_fechahora = "%Y-%m-%d %H:%M:%S.u"
    formato_fecha = "%Y-%m-%d"

    try:
        estacion_id = int(request.POST.get('estacion_id', None))
        variable_id = int(request.POST.get('variable_id', None))
    except:
        estacion_id = None
        variable_id = None

    cambios_json = request.POST.get('cambios', None)

    #TODO chequear porque si es la funcion ya está creada sin EXECUTE, no tendría problema de SQL INJECTION
    comentario = request.POST.get('comentario_general', None)

    resultado = False
    with connection.cursor() as cursor:
        cursor.callproc('insertar_' + str(variable_id) + 'validacion', [estacion_id, cambios_json])
        resultado = cursor.fetchone()[0]
        t = Thread(target=stack_reportes, args=(variable_id,))
        t.start()
    if resultado:
        cambios_lista = json.loads(cambios_json)
        fecha_inicio_dato = cambios_lista[0]['fecha']
        fecha_fin_dato = cambios_lista[-1]['fecha']
        Validacion(
            var_id_id=variable_id,
            est_id_id=estacion_id,
            fecha_validacion=datetime.date.today(),
            fecha_inicio_datos=fecha_inicio_dato,
            fecha_fin_datos=fecha_fin_dato,
            comentario=comentario
        ).save()
        lista = {'resultado': resultado}
        return JsonResponse(lista)
    return None


class ValidacionList(PermissionRequiredMixin, ListView, FormView):
    model = Validacion
    paginate_by = 12
    template_name = 'validacion/validacion_list.html'
    form_class = ConsultaValidacionForm
    permission_required = 'validacion.view_validacion'

    def post(self, request, *args, **kwargs):
        form = ConsultaValidacionForm(self.request.POST or None)
        if form.is_valid() and self.request.is_ajax():
            self.object_list = form.filtrar(form)
        else:
            self.object_list = Validacion.objects.all()
        context = super(ValidacionList, self).get_context_data(**kwargs)
        # Nota: no necesita recoger kwargs cuando en URLs se usa nombre código 'page'
        context.update(pagination(self.object_list, context['page_obj'].number, self.paginate_by))
        return render(request, 'validacion/validacion_table.html', context)


class ValidacionDetail(PermissionRequiredMixin, DetailView):
    model = Validacion
    permission_required = 'validacion.view_validacion'


def pagination(lista, page, num_reg):
    paginator = Paginator(lista, num_reg)
    if page is None:
        page = 1
    else:
        page = int(page)
    if page == 1:
        start = 1
        last = start + 1
    elif page == paginator.num_pages:
        last = paginator.num_pages
        start = last - 1
    else:
        start = page - 1
        last = page + 1
    context = {
        'first': '1',
        'last': paginator.num_pages,
        'range': range(start, last + 1),
    }
    return context


class PeriodosValidacion(PermissionRequiredMixin, FormView):
    template_name = 'validacion/periodos_validacion.html'
    form_class = ValidacionForm
    success_url = reverse_lazy('validacion:validar')
    lista = []
    permission_required = 'validacion.hidro_validar'

    def post(self, request, *args, **kwargs):
        estacion_id = None
        variable_id = None
        try:
            estacion_id = int(request.POST.get('estacion', None))
            variable_id = int(request.POST.get('variable', None))
        except:
            pass
        intervalos = periodos_validacion(est_id=estacion_id, var_id=variable_id)
        return render(request, self.template_name, {'intervalos': intervalos})


class BorrarValidados(PermissionRequiredMixin, FormView):
    template_name = 'validacion/borrar_validados.html'
    form_class = BorrarForm
    success_url = reverse_lazy('validacion:borrar_validados')
    resultado = None
    permission_required = 'validacion.hidro_borrar_solo_validados'

    def form_valid(self, form):
        try:
            if 'admin' not in self.request.user.username:
                return None
        except:
            return None

        estacion_id = form.cleaned_data['estacion'].est_id
        var_id = form.cleaned_data['variable'].var_id
        inicio = form.cleaned_data['inicio']
        fin = form.cleaned_data['fin']

        filas_validado, filas_horario, filas_diario, filas_mensual = borrar_validados(estacion_id, var_id, inicio, fin)

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


class BorrarCrudosYValidados(PermissionRequiredMixin, FormView):
    template_name = 'validacion/borrar_crudos_y_validados.html'
    form_class = BorrarForm
    success_url = reverse_lazy('validacion:borrar_crudos_y_validados')
    resultado = None
    permission_required = 'validacion.hidro_borrar_crudos_y_validados'

    def form_valid(self, form):
        try:
            if 'admin' not in self.request.user.username:
                return None
        except:
            return None

        estacion_id = form.cleaned_data['estacion'].est_id
        var_id = form.cleaned_data['variable'].var_id
        inicio = form.cleaned_data['inicio']
        fin = form.cleaned_data['fin']

        filas_crudo  = borrar_crudos(estacion_id, var_id, inicio, fin)
        filas_validado, filas_horario, filas_diario, filas_mensual = borrar_validados(estacion_id, var_id, inicio, fin)


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


class Validar(PermissionRequiredMixin, FormView):
    permission_required = 'validacion.hidro_validar'
    template_name = 'validacion/validar.html'
    form_class = ValidacionForm
    success_url = reverse_lazy('validacion:validar')

    def post(self, request, *args, **kwargs):
        form = ValidacionForm(self.request.POST or None)
        if form.is_valid():
            lista = reporte_validacion(form)
            variable = form.cleaned_data['variable']
            estacion = form.cleaned_data['estacion']
            _grafico = grafico(lista, variable,  estacion)
            inicio = form.cleaned_data['inicio']
            fin = form.cleaned_data['fin']
            return render(request, 'validacion/validar_tabla.html',
                          {'lista': lista,
                           'variable': variable,
                           'estacion': estacion,
                           'grafico': _grafico,
                           'inicio': inicio,
                           'fin': fin}
                          )
        return ""


@permission_required('validacion.calidad_validar')
def view_profundidades(request):
    try:
        estacion_id = int(request.GET.get('estacion_id', None))
    except:
        estacion_id = None

    try:
        variable_id = int(request.GET.get('variable_id', None))
    except:
        variable_id = None
    lista = profundidades(estacion_id, variable_id)

    return JsonResponse(lista)


class CalidadValidar(PermissionRequiredMixin, FormView):
    permission_required = 'validacion.calidad_validar'
    template_name = 'validacion/calidad_validar.html'
    form_class = ValidacionCalidadForm
    success_url = reverse_lazy('validacion:calidad_validar')

    def post(self, request, *args, **kwargs):
        form = ValidacionCalidadForm(self.request.POST or None)
        form.is_valid()

        try:
            variable = form.cleaned_data['variable']
            estacion = form.cleaned_data['estacion']
            profundidad = int(form.data['profundidad'])
            inicio = form.cleaned_data['inicio']
            fin = form.cleaned_data['fin']
        except:
            return HttpResponse('')

        tabla = reporte_validacion_profundidad(variable.var_id, estacion.est_id, profundidad, inicio, fin)
        _grafico = grafico(tabla, variable, estacion)

        return render(request, 'validacion/calidad_validar_tabla.html',
                      {'tabla': tabla,
                       'variable': variable,
                       'estacion': estacion,
                       'grafico': _grafico,
                       'inicio': inicio,
                       'fin': fin
                       })



class CalidadPeriodosValidacion(PermissionRequiredMixin, FormView):
    template_name = 'validacion/periodos_validacion.html'
    form_class = ValidacionCalidadForm
    permission_required = 'validacion.calidad_validar'

    def post(self, request, *args, **kwargs):
        form = ValidacionCalidadForm(self.request.POST or None)
        form.is_valid()
        try:
            variable = form.cleaned_data['variable']
            estacion = form.cleaned_data['estacion']
            profundidad = int(form.data['profundidad'])
        except:
            return HttpResponse('')
        intervalos = periodos_validacion_profundidad(est_id=estacion.est_id,
                                                               var_id=variable.var_id,
                                                               profundidad=profundidad)
        return render(request, self.template_name, {'intervalos': intervalos})


class CalidadBorrarDatos(PermissionRequiredMixin, FormView):
    template_name = 'validacion/calidad_borrar_datos.html'
    form_class = CalidadBorrarDatosForm
    success_url = reverse_lazy('validacion:calidad_borrar_datos')
    permission_required = 'validacion.calidad_validar'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form.is_valid()
        try:
            tipo = form.cleaned_data['tipo']
            estacion = form.cleaned_data['estacion'].est_id
            variable = form.cleaned_data['variable'].var_id
            profundidad = int(form.data['profundidad'])
            inicio = form.cleaned_data['inicio']
            fin = form.cleaned_data['fin']
        except:
            return super().form_valid(form)

        crudos = validados = horarios = diarios = mensuales = 0
        if '0' in tipo:
            crudos = borrar_crudos_profundidad(estacion, profundidad, variable, inicio, fin)
        if '1' in tipo:
            validados, horarios, diarios, mensuales = borrar_validados_profundidad(estacion, profundidad, variable, inicio, fin)

        if self.request.is_ajax():
            data = {
                'crudos' : crudos,
                'validados': validados,
                'horarios': horarios,
                'diarios': diarios,
                'mensuales': mensuales
            }
            return JsonResponse(data)
        else:
            return super().form_valid(form)