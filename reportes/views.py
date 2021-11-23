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

from estacion.models import Cuenca, SitioCuenca
from reportes.functions import *
from reportes.forms import *
from django.views.generic import FormView
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Prefetch
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
import os
import mimetypes
import matplotlib
import urllib
matplotlib.use('Agg')


class ReportesAnuario(PermissionRequiredMixin, FormView):
    permission_required = 'reportes.view_anuario'
    template_name = 'reportes/anuario_reporte.html'
    form_class = AnuarioForm
    success_url = reverse_lazy('reportes:anuario')

    def post(self, request, *args, **kwargs):
        form = AnuarioForm(self.request.POST or None)
        if form.is_valid():
            estacion=form.cleaned_data['estacion']
            año=form.cleaned_data['anio']
            _anuario = anuario(estacion, año)
            context = self.get_context_data(form=form)
            context.update(_anuario)
            return self.render_to_response(context)
        return render(request, self.template_name, {'form': form, 'mensaje': 'Formulario inválido.'})


# vista para comparar tres estaciones una sola variable
class ComparacionReporte(PermissionRequiredMixin, FormView):
    permission_required = 'reportes.view_comparacionvalores'
    template_name = 'reportes/comparacion_reporte.html'
    form_class = ComparacionForm
    success_url = reverse_lazy('reportes:comparacion_reporte')

    def post(self, request, *args, **kwargs):
        form = ComparacionForm(self.request.POST or None)
        if self.request.is_ajax():
            if form.is_valid():
                _grafico = comparar(form)
                return render(request, 'reportes/grafico.html', {'grafico': _grafico})
            return JsonResponse({'mensaje': 'Formulario no pasó la validación.'})


# vista para comparar 2 estaciones y dos Variables
class ComparacionVariables(PermissionRequiredMixin, FormView):
    permission_required = 'reportes.view_comparacionvariables'
    template_name = 'reportes/comparacion_variables.html'
    form_class = VariableForm
    success_url = reverse_lazy('reportes:comparacion_variables')

    def post(self, request, *args, **kwargs):
        form = VariableForm(self.request.POST or None)
        if self.request.is_ajax():
            if form.is_valid():
                _grafico = comparar_variable(form)
                return render(request, 'reportes/grafico.html', {'grafico': _grafico})
        return JsonResponse({'mensaje': 'Formulario no pasó la validación.'})


class ConsultasPeriodo(PermissionRequiredMixin, FormView):
    permission_required = 'reportes.view_consultasperiodo'
    template_name = 'reportes/consultas_periodo.html'
    form_class = ConsultasForm
    success_url = reverse_lazy('reportes:consultas_periodo')

    def post(self, request, *args, **kwargs):
        form = ConsultasForm(self.request.POST, {'user': request.user})
        if not form.is_valid():
            if self.request.is_ajax():
                return JsonResponse({'mensaje': 'Formulario no pasó la validación.'})
            else:
                return render(request, self.template_name, {'form': form, 'mensaje': 'Formulario inválido.'})

        variable = form.cleaned_data['variable']
        estacion_id = form.cleaned_data['estacion_id']
        estacion = Estacion.objects.get(pk=estacion_id)
        inicio = form.cleaned_data['inicio']
        fin = form.cleaned_data['fin']
        frecuencia = form.cleaned_data["frecuencia"]
        excluir_vacios = form.cleaned_data["excluir_vacios"]

        if self.request.is_ajax():
            # data_graf = getDatos_grafico2(estacion, variable, inicio, fin, frecuencia, excluir_vacios=excluir_vacios)
            data_graf = getDatos_grafico(estacion, variable, inicio, fin, frecuencia, excluir_vacios=excluir_vacios)
            return JsonResponse(data_graf)

        response = None
        if 'accion' not in request.POST:
            return
        if request.POST['accion'] == 'csv':
            response = export_csv(estacion, variable, inicio, fin, frecuencia, excluir_vacios=excluir_vacios)
        elif request.POST['accion'] == 'excel':
            response = export_excel(estacion, variable, inicio, fin, frecuencia, excluir_vacios=excluir_vacios)

        if response:
            return response
        mensaje = "No hay datos (" + frecuencia.nombre + ") en estación " + \
                       estacion.est_codigo + " en " + variable.var_nombre + " en el período seleccionado."
        return render(request, self.template_name, {'form': form, 'mensaje': mensaje})

    def get_form_kwargs(self):
        kwargs = super(ConsultasPeriodo, self).get_form_kwargs()
        kwargs.update({'user': self.request.user })
        return kwargs


class CalidadConsultasPeriodo(PermissionRequiredMixin, FormView):
    permission_required = 'reportes.view_calidadconsultasperiodo'
    template_name = 'reportes/calidad_consultas_periodo.html'
    form_class = CalidadConsultasForm
    success_url = reverse_lazy('reportes:calidad_consultas_periodo')

    def post(self, request, *args, **kwargs):
        form = CalidadConsultasForm(self.request.POST, {'user': request.user})
        if not form.is_valid():
            if self.request.is_ajax():
                return JsonResponse({'mensaje': 'Formulario no pasó la validación.'})
            else:
                return render(request, self.template_name, {'form': form, 'mensaje': 'Formulario inválido.'})
        variable = form.cleaned_data['variable']
        estacion_id = form.cleaned_data['estacion_id']
        estacion = Estacion.objects.get(pk=estacion_id)
        profundidad = int(form.cleaned_data['profundidad'])
        inicio = form.cleaned_data['inicio']
        fin = form.cleaned_data['fin']
        frecuencia = form.cleaned_data["frecuencia"]
        if self.request.is_ajax():
            graf1 = getGrafico(estacion, variable, inicio, fin, frecuencia, profundidad=profundidad)
            return render(request, 'reportes/porPeriodo.html',    {'grafico': graf1})

        response = None
        if 'accion' not in request.POST:
            return
        if request.POST['accion'] == 'csv':
            response = export_csv(estacion, variable, inicio, fin, frecuencia, profundidad=profundidad)
            if response: return response
        elif request.POST['accion'] == 'excel':
            response = export_excel(estacion, variable, inicio, fin, frecuencia, profundidad=profundidad)
        if response:
            return response
        mensaje = "No hay datos (" + frecuencia.nombre + ") en estación " +\
                           estacion.est_codigo + " en " + variable.var_nombre + " en el período seleccionado."
        return render(request, self.template_name, {'form': form, 'mensaje': mensaje})

    def get_form_kwargs(self):
        kwargs = super(CalidadConsultasPeriodo, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


@permission_required('reportes.reportes_general')
def variables(request):
    try:
        estacion_id = int(request.GET.get('estacion_id', None))
    except ValueError:
        estacion_id = None

    lista = {}
    if estacion_id is not None:
        variables = Cruce.objects.prefetch_related(
            Prefetch('var_id', queryset=Variable.objects.all())
        ).filter(est_id=estacion_id)
        for row in variables:
            lista[row.var_id.var_id] = row.var_id.var_nombre
    else:
        variables = Variable.objects.all()
        for row in variables:
            lista[row.var_id] = row.var_nombre
    return JsonResponse(lista)


@permission_required('reportes.reportes_general')
def cuencas(request):
    try:
        sitio_id = int(request.GET.get('sitio_id', None))
    except ValueError:
        sitio_id = None
    if sitio_id is not None:
        cuencas = SitioCuenca.objects.prefetch_related(
            Prefetch('cuenca', queryset=Cuenca.objects.all())
        ).filter(sitio_id=sitio_id)
    else:
        cuencas = SitioCuenca.objects.all()
    lista = {}
    for row in cuencas:
        try:
            lista[row.cuenca.id] = row.cuenca.nombre
        except:
            pass
    return JsonResponse(lista)


class Diario(PermissionRequiredMixin, FormView):
    permission_required = 'reportes.view_diario'
    template_name = 'reportes/diario.html'
    form_class = DiarioForm
    success_url = reverse_lazy('reportes:diario')

    def post(self, request, *args, **kwargs):
        form = DiarioForm(self.request.POST)
        if form.is_valid():
            variable = form.cleaned_data['variable']
            estacion_id = form.cleaned_data['estacion_id']
            estacion = Estacion.objects.get(pk=estacion_id)
            año = int(form.cleaned_data['año'])
            if not self.request.is_ajax():
                response = export_diario(estacion, variable, año)
                if response: return response
                mensaje = "No hay datos en estación " + estacion.est_codigo + " en " + variable.var_nombre + " " + str(año)
                return render(request, self.template_name, {'form': form, 'mensaje': mensaje})
        return render(request, self.template_name, {'form': form, 'mensaje': 'Formulario inválido.'})


class MensualMultianual(PermissionRequiredMixin, FormView):
    permission_required = 'reportes.view_mensualmultianual'
    template_name = 'reportes/mensual_multianual.html'
    form_class = MensualMultianualForm
    success_url = reverse_lazy('reportes:mensual_multianual')

    def post(self, request, *args, **kwargs):
        form = MensualMultianualForm(self.request.POST or None)
        if form.is_valid():
            variable = form.cleaned_data['variable']
            estacion_id = form.cleaned_data['estacion_id']
            estacion = Estacion.objects.get(pk=estacion_id)
            inicio = int(form.cleaned_data['año_inicio'])
            fin = int(form.cleaned_data['año_fin'])
            if not self.request.is_ajax():
                response = export_mensual_multianual(estacion, variable, inicio, fin)
                if response: return response
                mensaje = "No hay datos en " + estacion.est_codigo + \
                               " para " + variable.var_nombre + " en años seleccionados."
                return render(request, self.template_name, {'form': form, 'mensaje': mensaje})
            return render(request, self.template_name, {'form': form, 'mensaje': 'Formulario inválido.'})


@permission_required('reportes.view_manual')
def manual(request):
    file_path = "media/documents/Manual_de_Usuario.pdf"
    output_filename =  "Manual_de_Usuario.pdf"
    fp = open(file_path, 'rb')
    response = HttpResponse(fp.read())
    fp.close()
    type, encoding = mimetypes.guess_type(output_filename)
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    response['Content-Length'] = str(os.stat(file_path).st_size)
    if encoding is not None:
        response['Content-Encoding'] = encoding

    # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        #filename_header = 'filename=%s' % output_filename.encode('utf-8')
        filename_header = 'filename=%s' % urllib.parse.quote(output_filename.encode('utf-8'))
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        #filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(output_filename.encode('utf-8'))
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.parse.quote(output_filename.encode('utf-8'))
    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response


# Usa un modelo antiguo "Medicion" del SEDC
# # web service para consultar datos horarios
# def datos_json_horarios(request, est_id, var_id, fec_ini, fec_fin):
#     datos = datos_horarios_json(est_id, var_id, fec_ini, fec_fin)
#     return JsonResponse(datos, safe=False)
