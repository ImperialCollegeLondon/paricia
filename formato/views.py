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
from .models import Fecha, Hora, Formato, Extension, Delimitador, Clasificacion, Asociacion
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import ClasificacionForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.db.models import Value
from django.db.models.functions import Concat
from home.functions import *


#################################################################
# Fecha
class FechaCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'formato.add_fecha'
    model = Fecha
    fields = ['fec_formato', 'fec_codigo']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear"
        return context


class FechaList(PermissionRequiredMixin, TemplateView):
    permission_required = 'formato.view_fecha'
    template_name = 'formato/fecha_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = ['fec_id', 'fec_formato', 'fec_codigo']
        modelo = Fecha.objects.values_list(*campos)
        context['fechas'] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class FechaDetail(PermissionRequiredMixin, DetailView):
    model = Fecha
    permission_required = 'formato.view_fecha'


class FechaUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'formato.change_fecha'
    model = Fecha
    fields = ['fec_formato', 'fec_codigo']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class FechaDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'formato.delete_fecha'
    model = Fecha
    success_url = reverse_lazy('formato:fecha_index')

#################################################################
# Hora
class HoraCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'formato.add_hora'
    model = Hora
    fields = ['hor_formato', 'hor_codigo']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear"
        return context


class HoraList(PermissionRequiredMixin, TemplateView):
    permission_required = 'formato.view_hora'
    template_name = 'formato/hora_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = ['hor_id', 'hor_formato', 'hor_codigo']
        modelo = Hora.objects.values_list(*campos)
        context['horas'] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class HoraDetail(PermissionRequiredMixin, DetailView):
    model =Hora
    permission_required = 'formato.view_hora'



class HoraUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'formato.change_hora'
    model = Hora
    fields = ['hor_formato', 'hor_codigo']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class HoraDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'formato.delete_hora'
    model = Hora
    success_url = reverse_lazy('formato:hora_index')

#################################################################

class FormatoCreate(PermissionRequiredMixin, CreateView):
    model = Formato
    fields = ['for_nombre', 'for_descripcion', 'ext_id', 'del_id', 'for_fil_ini', 'for_fil_cola', 'for_col_fecha',
              'fec_id', 'for_col_hora', 'hor_id', 'es_fecha_utc']
    permission_required = 'formato.add_formato'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear"
        return context


class FormatoList(PermissionRequiredMixin, TemplateView):
    template_name = 'formato/formato_list.html'
    permission_required = 'formato.view_formato'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = ['for_id', 'for_nombre', 'for_descripcion', 'ext_id__ext_valor', 'del_id__del_nombre', 'for_fil_ini',
                  'for_fil_cola', 'for_col_fecha', 'fec_id__fec_formato', 'es_fecha_utc', 'for_col_hora',
                  'hor_id__hor_formato']
        modelo = Formato.objects.values_list(*campos)
        context['formato'] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class FormatoDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'formato.view_formato'
    model = Formato

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        variable = Clasificacion.objects.filter(for_id=self.object.for_id)
        context['variable'] = variable
        return context


class FormatoUpdate(PermissionRequiredMixin, UpdateView):
    model = Formato
    permission_required = 'formato.change_formato'
    fields = ['ext_id', 'del_id', 'for_nombre', 'for_descripcion',
              'for_fil_ini', 'for_fil_cola', 'fec_id', 'for_col_fecha', 'hor_id', 'for_col_hora', 'es_fecha_utc']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class FormatoDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'formato.delete_formato'
    model = Formato
    success_url = reverse_lazy('formato:formato_index')


# Extension
class ExtensionCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'formato.add_extension'
    model = Extension
    fields = ['ext_valor']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear"
        return context


class ExtensionList(PermissionRequiredMixin, TemplateView):
    permission_required = 'formato.view_extension'
    template_name = 'formato/extension_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = ['ext_id', 'ext_valor']
        modelo = Extension.objects.values_list(*campos)
        context['extension'] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class ExtensionUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'formato.change_extension'
    model = Extension
    fields = ['ext_valor']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class ExtensionDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'formato.delete_extension'
    model = Extension
    success_url = reverse_lazy('formato:extension_index')


# Delimitador
class DelimitadorCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'formato.add_delimitador'
    model = Delimitador
    fields = ['del_nombre', 'del_caracter']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear"
        return context


class DelimitadorList(PermissionRequiredMixin, TemplateView):
    permission_required = 'formato.view_delimitador'
    template_name = 'formato/delimitador_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = ['del_id', 'del_nombre', 'del_caracter']
        modelo = Delimitador.objects.values_list(*campos)
        context['delimitador'] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class DelimitadorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'formato.change_delimitador'
    model = Delimitador
    fields = ['del_nombre', 'del_caracter']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class DelimitadorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'formato.delete_delimitador'
    model = Delimitador
    success_url = reverse_lazy('formato:delimitador_index')


# Clasificacion
class ClasificacionCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'formato.add_clasificacion'
    model = Clasificacion
    fields = ['var_id', 'acumular', 'incremental', 'resolucion', 'coma_decimal',
              'cla_valor', 'col_validador_valor', 'txt_validador_valor',
              'cla_maximo', 'col_validador_maximo', 'txt_validador_maximo',
              'cla_minimo', 'col_validador_minimo', 'txt_validador_minimo'
              ]

    def post(self, request, *args, **kwargs):
        form = ClasificacionForm(self.request.POST or None)
        clasificacion = form.save(commit=False)
        for_id = kwargs.get('for_id')
        formato = Formato.objects.get(for_id=for_id)
        clasificacion.for_id = formato
        clasificacion.save()
        url = reverse('formato:formato_detail', kwargs={'pk': formato.for_id})
        return HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear"
        for_id = self.kwargs.get('for_id')
        context['url'] = reverse('formato:clasificacion_create', kwargs={'for_id': for_id})
        return context


class ClasificacionUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'formato.change_clasificacion'
    model = Clasificacion
    fields = ['for_id', 'var_id', 'acumular', 'incremental', 'resolucion', 'coma_decimal',
              'cla_valor', 'col_validador_valor', 'txt_validador_valor',
              'cla_maximo', 'col_validador_maximo', 'txt_validador_maximo',
              'cla_minimo', 'col_validador_minimo', 'txt_validador_minimo'
              ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar"
        cla_id = self.kwargs.get('pk')
        context['url'] = reverse('formato:clasificacion_update', kwargs={'pk': cla_id})
        context['for_id'] = self.object.for_id.for_id
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        for_id = data.get('for_id')
        self.success_url =  reverse('formato:formato_detail', kwargs={'pk': for_id})
        return super().post(data, **kwargs)


class ClasificacionDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'formato.delete_clasificacion'
    model = Clasificacion

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        formato = self.object.for_id
        self.object.delete()
        return HttpResponseRedirect(reverse('formato:formato_detail', kwargs={'pk': formato.for_id}))


class ClasificacionDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'formato.view_clasificacion'
    model = Clasificacion


# Asociacion
class AsociacionCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'formato.add_asociacion'
    model = Asociacion
    fields = ['for_id', 'est_id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear"
        return context


class AsociacionList(PermissionRequiredMixin, TemplateView):
    permission_required = 'formato.view_asociacion'
    template_name = 'formato/asociacion_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = ['aso_id', 'for_id__for_nombre', 'est_id__est_codigo']
        asociacion = Asociacion.objects.all().values_list(*campos)
        context['asociacion'] = modelo_a_tabla_html(asociacion, col_extra=True)
        return context


class AsociacionDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'formato.view_asociacion'
    model = Asociacion


class AsociacionUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'formato.change_asociacion'
    model = Asociacion
    fields = ['for_id', 'est_id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class AsociacionDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'formato.delete_asociacion'
    model = Asociacion
    success_url = reverse_lazy('formato:asociacion_index')
