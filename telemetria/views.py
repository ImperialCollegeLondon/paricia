from django.views.generic import FormView, ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import *
from .functions import *
from .models import *
from django.urls import reverse_lazy
from home.functions import pagination


class ConsultaForm(FormView):
    template_name = 'telemetria/visualizar.html'
    form_class = ConsultaForm


def Consulta(request):
    try:
        estacion_id = int(request.POST.get('estacion', None))
    except ValueError:
        estacion_id = None

    try:
        inicio = request.POST.get('inicio', None)
        if len(inicio) is not 10:
            inicio = None
    except ValueError:
        inicio = None

    lista = consulta(estacion_id, inicio)
    return JsonResponse(lista)


class ConfigVisualizarList(ListView):
    model = ConfigVisualizar
    paginate_by = 15
    ordering = ['estacion', 'variable']

    def get_context_data(self, **kwargs):
        context = super(ConfigVisualizarList, self).get_context_data(**kwargs)
        page = self.request.resolver_match.kwargs.get('page')
        context.update(pagination(self.object_list, page, self.paginate_by))
        return context


class ConfigVisualizarDetail(DetailView):
    model = ConfigVisualizar


class ConfigVisualizarCreate(CreateView):
    model = ConfigVisualizar
    fields = ['estacion', 'variable', 'umbral_superior', 'umbral_inferior']
    success_url = "/telemetria/visualizar/config"


class ConfigVisualizarUpdate(UpdateView):
    model = ConfigVisualizar
    fields = ['estacion', 'variable', 'umbral_superior', 'umbral_inferior']


class ConfigVisualizarDelete(DeleteView):
    model = ConfigVisualizar
    success_url = reverse_lazy('telemetria:configvisualizar_list')


#########################


class ConfigAlarmaList(ListView):
    model = AlarmaEmail

    def get_context_data(self, **kwargs):
        context = super(ConfigAlarmaList, self).get_context_data(**kwargs)
        try:
            context['lim_inf_horas'] = TeleVariables.objects.get(nombre='ALAR_TRAN_LIMI_INFE').valor
            context['lim_sup_horas'] = TeleVariables.objects.get(nombre='ALAR_TRAN_LIMI_SUPE').valor
        except TeleVariables.DoesNotExit:
            context['lim_inf_horas'] = None
            context['lim_sup_horas'] = None
        return context


class ConfigAlarmaEmailCreate(CreateView):
    model = AlarmaEmail
    fields = ['email']
    success_url = reverse_lazy("telemetria:config_alarma_list")


class ConfigAlarmaEmailDelete(DeleteView):
    model = AlarmaEmail
    success_url = reverse_lazy('telemetria:config_alarma_list')

class ConfigAlarmaTransmisionLimites(FormView):
    template_name = 'telemetria/config_alarma_transmision_limites.html'
    form_class = AlarmaTransmisionLimitesForm


##########################

class MapaTransmision(TemplateView):
    template_name = 'telemetria/mapa_transmision.html'


def MapaTransmisionConsulta(request):
    resultado = consulta_alarma_transmision()
    return JsonResponse(resultado)


############################

class PrecipitacionView(FormView):
    template_name = 'telemetria/precipitacion.html'
    form_class = PrecipitacionForm


@login_required
def consulta_precipitacion(request):
    try:
        estacion_id = int(request.POST.get('estacion', None))
    except ValueError:
        estacion_id = None

    try:
        inicio = request.POST.get('inicio', None)
        if len(inicio) is not 10:
            inicio = None
    except ValueError:
        inicio = None

    try:
        fin = request.POST.get('fin', None)
        if len(fin) is not 10:
            fin = None
    except ValueError:
        fin = None

    lista = datos_precipitacion(estacion_id, inicio, fin)
    return JsonResponse(lista)


class PrecipitacionMultiestacionView(FormView):
    template_name = 'telemetria/precipitacion_multiestacion.html'
    form_class = PrecipitacionMultiestacionForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            estaciones = request.POST.getlist('estacion')
            inicio = request.POST.get('inicio')
            fin = request.POST.get('fin')
            lista = datos_precipitacion_multiestacion(estaciones, inicio, fin)
            return JsonResponse(lista)

