from django.views.generic.base import TemplateView
from django.views.generic import FormView
from reportes.forms import AnuarioForm
from reportes.consultas.forms import MedicionSearchForm, ComparacionForm, VariableForm
import csv
from django.http import HttpResponse
# from django.template import loader, Context
from reportes.consultas.functions import (grafico, datos_horarios_json, datos_diarios, datos_5minutos, datos_horarios,
                                          datos_instantaneos, datos_mensuales)
from reportes.functions import filtrar, comparar, comparar_variable
from django.shortcuts import render
from django.http import JsonResponse


class ReportesAnuario(FormView):
    template_name = 'reportes/anuario_reporte.html'
    form_class = AnuarioForm
    success_url = '/reportes/anuario/'
    lista = {}

    '''def post(self, request, *args, **kwargs):
        form = AnuarioForm(self.request.POST or None)
        if form.is_valid():
            self.lista = filtrar(form)
        return self.render_to_response(self.get_context_data(form=form))'''

    def post(self, request, *args, **kwargs):
        form = AnuarioForm(self.request.POST or None)
        if form.is_valid():
            if self.request.is_ajax():
                self.lista = filtrar(form)
                return render(request,'reportes/anuario/anuario.html',self.lista)
        return self.render_to_response(self.get_context_data(form=form))
    def get_context_data(self, **kwargs):
        context = super(ReportesAnuario, self).get_context_data(**kwargs)
        context.update(self.lista)
        return context


# vista para comparar tres estaciones una sola variable
class ComparacionValores(FormView):
    template_name = 'reportes/comparacion_reporte.html'
    form_class = ComparacionForm
    success_url = '/reportes/comparacion/'
    grafico = []

    def post(self, request, *args, **kwargs):
        form = ComparacionForm(self.request.POST or None)
        if form.is_valid():

            if self.request.is_ajax():
                self.grafico = comparar(form)
                return render(request, 'reportes/consultas/grafico.html',
                              {'grafico': self.grafico})

        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(ComparacionValores, self).get_context_data(**kwargs)
        context.update({'grafico': self.grafico})
        return context


# vista para comparar 2 estaciones y dos Variables
class ComparacionVariables(FormView):
    template_name = 'reportes/comparacion_variable.html'
    form_class = VariableForm
    success_url = '/reportes/compararvariable/'
    grafico = []

    def post(self, request, *args, **kwargs):
        form = VariableForm(self.request.POST or None)
        if form.is_valid():
            if self.request.is_ajax():
                self.grafico = comparar_variable(form)
                return render(request, 'reportes/consultas/grafico.html',
                              {'grafico': self.grafico})
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(ComparacionVariables, self).get_context_data(**kwargs)
        context.update({'grafico': self.grafico})
        return context


# consultas por periodo y frecuencia horaria, diaria y mensual
class ConsultasPeriodo(FormView):
    template_name = 'reportes/consultas_periodo.html'
    form_class = MedicionSearchForm
    success_url = '/reportes/consultas'
    frecuencia = str("")
    valores = []
    grafico = []

    def post(self, request, *args, **kwargs):
        form = MedicionSearchForm(self.request.POST or None)
        if form.is_valid():
            self.frecuencia = form.cleaned_data["frecuencia"]
            if self.request.is_ajax():
                # if form.exists(form):
                self.grafico = grafico(form)
                return render(request, 'reportes/consultas/grafico.html',
                              {'grafico': self.grafico, 'frecuencia': self.frecuencia})
            else:
                return self.export_datos(self.frecuencia, form)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(ConsultasPeriodo, self).get_context_data(**kwargs)
        # context['lista']=self.lista
        # context['frecuencia']=self.frecuencia
        # context['valores']=self.valores
        context['grafico'] = self.grafico
        return context

    def export_datos(self, frecuencia, form):
        estacion = form.cleaned_data['estacion']
        variable = form.cleaned_data['variable']
        fecha_inicio = form.cleaned_data['inicio']
        fecha_fin = form.cleaned_data['fin']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reporte.csv"'
        writer = csv.writer(response)
        if frecuencia == "0":
            valores, maximos, minimos, tiempo = datos_instantaneos(estacion, variable, fecha_inicio, fecha_fin)
        elif frecuencia == "1":
            valores, maximos, minimos, tiempo = datos_5minutos(estacion, variable, fecha_inicio, fecha_fin)
        elif frecuencia == "2":
            valores, maximos, minimos, tiempo = datos_horarios(estacion, variable, fecha_inicio, fecha_fin)
        elif frecuencia == "3":
            valores, maximos, minimos, tiempo = datos_diarios(estacion, variable, fecha_inicio, fecha_fin)
        else:
            valores, maximos, minimos, tiempo = datos_mensuales(estacion, variable, fecha_inicio, fecha_fin)

        writer.writerow(['fecha', 'valor', 'maximo', 'minimo'])
        for valor, maximo, minimo, fecha in zip(valores, maximos, minimos, tiempo):
            writer.writerow([fecha, valor, maximo, minimo])
        return response


# web service para consultar datos horarios
def datos_json_horarios(request, est_id, var_id, fec_ini, fec_fin):
    datos = datos_horarios_json(est_id, var_id, fec_ini, fec_fin)
    return JsonResponse(datos, safe=False)
