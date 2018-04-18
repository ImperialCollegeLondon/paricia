# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from validacion.models import Validacion
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from validacion.forms import ValidacionProcess
from validacion import functions
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin


class ValidacionCreate(LoginRequiredMixin, CreateView):
    model = Validacion
    fields = ['est_id', 'var_id', 'val_fecha', 'val_num_dat', 'val_fre_reg', 'val_porcentaje']

    def get_context_data(self, **kwargs):
        context = super(ValidacionCreate, self).get_context_data(**kwargs)
        context['title'] = "Crear"
        return context


class ValidacionList(LoginRequiredMixin, ListView):
    model = Validacion
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ValidacionList, self).get_context_data(**kwargs)
        lista = Validacion.objects.all()
        page = self.request.GET.get('page')
        context.update(pagination(self.object_list, page, 10))
        return context


class ValidacionDetail(LoginRequiredMixin, DetailView):
    model = Validacion


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


def procesar_validacion(request):
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


def pagination(lista, page, num_reg):
    # lista=model.objects.all()
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
