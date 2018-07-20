# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from registro.models import LogMedicion, LogMedicionSearchForm
from medicion.models import Medicion
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView

from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class LogMedicionList(LoginRequiredMixin, ListView, FormView):
    # parámetros ListView
    model = LogMedicion
    paginate_by = 10
    # parámetros FormView
    template_name = 'registro/logmedicion_list.html'
    form_class = LogMedicionSearchForm

    # parametros propios
    def post(self, request, *args, **kwargs):
        form = LogMedicionSearchForm(self.request.POST or None)
        page = kwargs.get('page')
        if form.is_valid():
            self.object_list = form.filtrar(form)
            if self.request.is_ajax():
                context = super(LogMedicionList, self).get_context_data(**kwargs)
                page = kwargs.get('page')
                context.update(pagination(self.object_list, page, 10))
                return render(request, 'registro/logmedicion_table.html', context)
        else:
            self.object_list = LogMedicion.objects.all()
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(LogMedicionList, self).get_context_data(**kwargs)
        page = kwargs.get('page')
        context.update(pagination(self.object_list, page, 10))
        return context


class LogMedicionDetail(LoginRequiredMixin, DetailView):
    model = LogMedicion
    template_name = 'registro/logmedicion_detail.html'

    def get_context_data(self, **kwargs):
        context = super(LogMedicionDetail, self).get_context_data(**kwargs)
        informacion = consultar_medicion(self.object)
        context['medicion'] = informacion
        return context


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


def consultar_medicion(logmedicion):
    year = logmedicion.med_fecha.strftime('%Y')
    var_cod = logmedicion.variable.var_codigo
    tabla = var_cod + '.m' + year
    sql = 'SELECT * FROM ' + tabla + ' WHERE '
    sql += 'med_id=' + str(logmedicion.medicion)
    consulta = list(Medicion.objects.raw(sql))
    return consulta[0]
