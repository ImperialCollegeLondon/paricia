# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Estacion, Inamhi   # , Registro
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import EstacionSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from home.functions import pagination
from django.http import JsonResponse, HttpResponse
import json

# Create your views here.
class EstacionCreate(LoginRequiredMixin, CreateView):
    model = Estacion
    fields = ['est_id', 'est_codigo', 'est_nombre', 'est_latitud',
              'est_longitud', 'est_altura', 'est_fecha_inicio', 'est_ficha', 'tipo', 'provincia', 'est_externa', 'influencia_km']

    def form_valid(self, form):
        return super(EstacionCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EstacionCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear"
        return context

    '''def model_form_upload(request):
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('index')
        else:
            form = DocumentForm()
        return render(request, 'core/model_form_upload.html', {
            'form': form
        })'''


class EstacionList(LoginRequiredMixin, ListView, FormView):
    # parámetros ListView
    model = Estacion
    paginate_by = 10
    # parámetros FormView
    template_name = 'estacion/estacion_list.html'
    form_class = EstacionSearchForm

    def post(self, request, *args, **kwargs):
        form = EstacionSearchForm(self.request.POST or None)
        page = kwargs.get('page')
        if form.is_valid() and self.request.is_ajax:
            self.object_list = form.filtrar(form)
        else:
            self.object_list = Estacion.objects.all()
        context = super(EstacionList, self).get_context_data(**kwargs)
        context.update(pagination(self.object_list, page, 10))
        return render(request, 'estacion/estacion_table.html', context)

    def get_context_data(self, **kwargs):
        context = super(EstacionList, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        context.update(pagination(self.object_list, page, 10))
        return context


class EstacionDetail(LoginRequiredMixin, DetailView):
    model = Estacion


class EstacionUpdate(LoginRequiredMixin, UpdateView):
    model = Estacion
    fields = ['est_id', 'est_codigo', 'est_nombre', 'est_latitud', 'est_longitud', 'est_altura',
              'est_fecha_inicio', 'est_ficha', 'tipo', 'provincia', 'est_estado','est_externa', 'influencia_km']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EstacionUpdate, self).get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class EstacionDelete(LoginRequiredMixin, DeleteView):
    model = Estacion
    success_url = reverse_lazy('estacion:estacion_index')


# Consulta de estaciones por codigo
def search_estaciones(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Estacion.objects.filter(est_codigo__startswith=q).filter(est_externa=False)
        results = []
        for r in search_qs:
            results.append(r.est_codigo)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


# estaciones FONAG  en formato JSON
def datos_json_estaciones(request):
    estaciones = list(Estacion.objects.order_by('est_id').filter(est_externa=False))
    # estaciones = list(Estacion.objects.order_by('est_id').all())
    features = []
    for item in estaciones:
        fila = dict(
            type='Feature',
            geometry=dict(
                type='Point',
                coordinates=[float(item.est_longitud), float(item.est_latitud)]
            ),
            properties=dict(
                codigo=item.est_codigo,
                nombre=item.est_nombre,
                tipo=item.tipo.tip_nombre,
                latitud=item.est_latitud,
                longitud=item.est_longitud,
                altura=item.est_altura
            )

        )
        features.append(fila)
    datos = dict(
        type='FeatureCollection',
        features=features
    )
    return JsonResponse(datos,safe=False)


# estaciones INAMHI en formato JSON
def estaciones_inamhi_json(request):
    estaciones = list(Inamhi.objects.order_by('id').all())
    features = []
    for item in estaciones:
        fila = dict(
            type='Feature',
            geometry=dict(
                type='Point',
                coordinates=[float(item.longitud), float(item.latitud)]
            ),
            properties=dict(
                codigo=item.codigo,
                nombre=item.nombre,
                tipo=item.categoria,
                latitud=item.latitud,
                longitud=item.longitud,
                altura=None
            )

        )
        features.append(fila)
    datos = dict(
        type='FeatureCollection',
        features=features
    )
    return JsonResponse(datos,safe=False)
