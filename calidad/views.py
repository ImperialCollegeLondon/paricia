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

from django.views.generic import FormView, TemplateView, CreateView, ListView, UpdateView, DetailView, DeleteView
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from .forms import *
from .functions import *
from .models import *
from django.urls import reverse_lazy
from django.shortcuts import render


class Grafico1View(PermissionRequiredMixin, FormView):
    permission_required = 'calidad.view_graficos'
    template_name = 'calidad/grafico1.html'
    form_class = Grafico1Form


@permission_required('calidad.view_graficos')
def consulta_grafico1(request):
    try:
        estacion_id = int(request.POST.get('estacion', None))
    except ValueError:
        estacion_id = None

    try:
        inicio = request.POST.get('inicio', None)
        if len(inicio) != 10:
            inicio = None
    except ValueError:
        inicio = None
        
    try:
        fin = request.POST.get('fin', None)
        if len(fin) != 10:
            fin = None
    except ValueError:
        fin = None
        
    try:
        variables = request.POST.getlist('variables', None)
    except ValueError:
        variables = None

    try:
        profundidad = int(request.POST.get('profundidad', None))
    except ValueError:
        profundidad = None

    lista = datos_grafico1(estacion_id, variables, profundidad, inicio, fin)
    return JsonResponse(lista)


class CrudosGrafico1View(PermissionRequiredMixin, FormView):
    permission_required = 'calidad.view_graficoscrudos'
    template_name = 'calidad/crudos_grafico1.html'
    form_class = Grafico1Form


@permission_required('calidad.view_graficoscrudos')
def consulta_crudos_grafico1(request):
    try:
        estacion_id = int(request.POST.get('estacion', None))
    except ValueError:
        estacion_id = None

    try:
        inicio = request.POST.get('inicio', None)
        if len(inicio) != 10:
            inicio = None
    except ValueError:
        inicio = None

    try:
        fin = request.POST.get('fin', None)
        if len(fin) != 10:
            fin = None
    except ValueError:
        fin = None

    try:
        variables = request.POST.getlist('variables', None)
    except ValueError:
        variables = None

    try:
        profundidad = int(request.POST.get('profundidad', None))
    except ValueError:
        profundidad = None

    lista = datos_crudos_grafico1(estacion_id, variables, profundidad, inicio, fin)
    return JsonResponse(lista)


class Grafico2View(PermissionRequiredMixin, FormView):
    permission_required = 'calidad.view_graficos'
    template_name = 'calidad/grafico2.html'
    form_class = Grafico1Form


@permission_required('calidad.view_graficos')
def consulta_grafico2(request):
    try:
        estacion_id = int(request.POST.get('estacion', None))
    except ValueError:
        estacion_id = None

    try:
        inicio = request.POST.get('inicio', None)
        if len(inicio) != 10:
            inicio = None
    except ValueError:
        inicio = None

    try:
        fin = request.POST.get('fin', None)
        if len(fin) != 10:
            fin = None
    except ValueError:
        fin = None

    try:
        variables = request.POST.getlist('variables', None)
    except ValueError:
        variables = None

    try:
        profundidad = int(request.POST.get('profundidad', None))
    except ValueError:
        profundidad = None

    lista = datos_grafico2(estacion_id, variables, profundidad, inicio, fin)
    return JsonResponse(lista)



class AsociacionHidroList(PermissionRequiredMixin, ListView):
    model = AsociacionHidro
    template_name = 'calidad/asociacionhidro_list.html'
    permission_required = 'calidad.view_asociacionhidro'


class AsociacionHidroCreate(PermissionRequiredMixin, CreateView):
    model = AsociacionHidro
    form_class = AsociacionHidroForm
    permission_required = 'calidad.add_asociacionhidro'
    success_url = reverse_lazy("calidad:asociacionhidro_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear"
        return context


class AsociacionHidroDetail(PermissionRequiredMixin, DetailView):
    model = AsociacionHidro
    permission_required = 'calidad.view_asociacionhidro'


class AsociacionHidroUpdate(PermissionRequiredMixin, UpdateView):
    model = AsociacionHidro
    permission_required = 'calidad.change_asociacionhidro'
    form_class = AsociacionHidroForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class AsociacionHidroDelete(PermissionRequiredMixin, DeleteView):
    model = AsociacionHidro
    permission_required = 'calidad.delete_asociacionhidro'
    success_url = reverse_lazy('calidad:asociacionhidro_index')


class CompararHidroView(PermissionRequiredMixin, FormView):
    permission_required = 'calidad.view_comparar_hidro'
    template_name = 'calidad/comparar_hidro.html'
    form_class = CompararHidroForm

    def get_form_kwargs(self):
        kwargs = super(CompararHidroView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


@permission_required('calidad.view_comparar_hidro')
def consulta_comparar_hidro(request):
    if request.method == "POST":
        form = CompararHidroForm(request.POST, user=request.user)
        if not form.is_valid():
            return None
        lista = datos_comparar_hidro( form.cleaned_data['frecuencia'],
                                      form.cleaned_data['inicio'],
                                      form.cleaned_data['fin'],
                                      form.cleaned_data['est_calidad'],
                                      form.cleaned_data['profundidad'],
                                      form.cleaned_data['var_calidad'],
                                      form.cleaned_data['est_hidro'],
                                      form.cleaned_data['var_hidro']
        )
    return JsonResponse(lista)


@permission_required('calidad.view_comparar_hidro')
def cargar_estaciones_hidro(request):
    est_calidad_id = request.GET.get('est_calidad_id')
    asociacion_hidro = AsociacionHidro.objects.get(estacion_calidad__pk=est_calidad_id)
    est_hidro = Estacion.objects.filter(
        pk__in=asociacion_hidro.estaciones_hidro.values_list('est_id', flat=True)
    )
    return render(request, 'calidad/cargar_estaciones_hidro.html', {'est_hidro': est_hidro})



class UsuarioVariableList(PermissionRequiredMixin, ListView):
    model = UsuarioVariable
    template_name = 'calidad/usuariovariable_list.html'
    permission_required = 'calidad.view_usuariovariable'


class UsuarioVariableCreate(PermissionRequiredMixin, CreateView):
    model = UsuarioVariable
    form_class = UsuarioVariableForm
    permission_required = 'calidad.add_usuariovariable'
    success_url = reverse_lazy("calidad:usuariovariable_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear"
        return context


class UsuarioVariableDetail(PermissionRequiredMixin, DetailView):
    model = UsuarioVariable
    permission_required = 'calidad.view_usuariovariable'


class UsuarioVariableUpdate(PermissionRequiredMixin, UpdateView):
    model = UsuarioVariable
    form_class = UsuarioVariableForm
    permission_required = 'calidad.change_usuariovariable'
    success_url = reverse_lazy("calidad:usuariovariable_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar"
        return context


class UsuarioVariableDelete(PermissionRequiredMixin, DeleteView):
    model = UsuarioVariable
    permission_required = 'calidad.delete_usuariovariable'
    success_url = reverse_lazy('calidad:usuariovariable_index')