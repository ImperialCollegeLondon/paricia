# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from anuarios.forms import AnuarioForm
from anuarios import functions
from django.http import JsonResponse
# Vista genérica para mostrar resultados
from django.views.generic.base import TemplateView
# Workbook nos permite crear libros en excel
from openpyxl import Workbook,load_workbook
# Nos devuelve un objeto resultado, en este caso un archivo de excel
from django.http.response import HttpResponse

from sedc.settings import BASE_DIR

# Create your views here.
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


# lista de variables por estacion
def lista_variables(request):
    estacion = request.GET.get('estacion', None)
    datos = functions.consultar_variables(estacion)
    return JsonResponse(datos)


# Reporte Excel
class ReportePersonasExcel(TemplateView):
    def get(self, request, *args, **kwargs):
        ruta = str(BASE_DIR) + '/media/anuario/AnuarioBase.xlsx'
        wb = load_workbook(ruta)
        ws=wb['H5006-AGLLA']
        ws['B13']=1
        # Establecemos el nombre del archivo
        nombre_archivo = "ReporteAnuario.xlsx"
        # Definimos que el tipo de respuesta a devolver es un archivo de microsoft excel
        response = HttpResponse(content_type="application/ms-excel")
        contenido = "attachment; filename={0}".format(nombre_archivo)
        response["Content-Disposition"] = contenido
        wb.save(response)
        return response
