from estacion.models import Inamhi
from variable.models import Parametro

from django.views.generic import FormView, TemplateView
from reportes.forms import AnuarioForm, InamhiForm
from reportes.consultas.forms import MedicionSearchForm, ComparacionForm, VariableForm, EstacionVariableSearchForm,UsuarioSearchForm
import csv
from django.http import HttpResponse

from reportes.consultas.functions import (datos_horarios_json, datos_instantaneos, datos_estacion, reporte_excel)
from reportes.functions import filtrar, comparar, comparar_variables, consultar_datos, procesar_json_inamhi, consultar_datos_usuario
from datetime import date
from django.shortcuts import render
from django.http import JsonResponse


class ReportesAnuario(FormView):
    template_name = 'reportes/anuario_normal.html'
    form_class = AnuarioForm
    success_url = '/reportes/anuario/'
    lista = {}

    def get_context_data(self, **kwargs):
        context = super(ReportesAnuario, self).get_context_data(**kwargs)
        context['base_template'] = get_vista_usuario(self.request)
        return context

    def post(self, request, *args, **kwargs):
        form = AnuarioForm(self.request.POST or None)
        if form.is_valid():
            context = super(ReportesAnuario, self).get_context_data(**kwargs)
            self.lista = filtrar(form)
            print(len(self.lista))
            context.update(self.lista)
            context['base_template'] = get_vista_usuario(self.request)
            return render(request, 'reportes/anuario_normal.html', context)

        return render(request, 'home/form_error.html', {'form': form})


# vista para comparar tres estaciones una sola variable
class ComparacionValores(FormView):
    template_name = 'reportes/comparacion_reporte.html'
    form_class = ComparacionForm
    success_url = '/reportes/comparacion/'
    grafico = []

    def get_context_data(self, **kwargs):
        context = super(ComparacionValores, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['base_template'] = "index.html"
        else:
            context['base_template'] = "index_invitado.html"
        return context

    def post(self, request, *args, **kwargs):
        form = ComparacionForm(self.request.POST or None)
        if form.is_valid() and self.request.is_ajax():
            plantilla = 'reportes/consultas/grafico.html'
            diccionario = comparar(form)
            return render(request, plantilla, diccionario)

        return render(request, 'home/form_error.html', {'form': form})


# vista para comparar 2 estaciones y dos Variables
class ComparacionVariables(FormView):
    template_name = 'reportes/comparacion_variable.html'
    form_class = VariableForm
    success_url = '/reportes/compararvariable/'
    grafico = []

    def get_context_data(self, **kwargs):
        context = super(ComparacionVariables, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['base_template'] = "index.html"
        else:
            context['base_template'] = "index_invitado.html"
        return context

    def post(self, request, *args, **kwargs):
        form = VariableForm(self.request.POST or None)
        if form.is_valid() and self.request.is_ajax():
            '''self.grafico = comparar_variable(form)
            plantilla = 'reportes/consultas/grafico.html'
            diccionario = {'grafico': self.grafico}
            return render(request, plantilla, diccionario)'''
            datos = comparar_variables(form)
            return JsonResponse(datos, safe=False)
        return render(request, 'home/form_error.html', {'form': form})


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
                '''self.grafico = grafico(form)
                return render(request, 'reportes/consultas/grafico.html',
                              {'grafico': self.grafico, 'frecuencia': self.frecuencia})'''
                datos = consultar_datos(form)
                return JsonResponse(datos, safe=False)
            else:
                if 'graficar' in request.POST:
                    context = super(ConsultasPeriodo, self).get_context_data(**kwargs)
                    context.update(consultar_datos(form))
                    context['base_template'] = get_vista_usuario(self.request)
                    return render(request, 'reportes/consultas_periodo.html', context)

                if self.frecuencia == "0":
                    return self.export_csv(form)
                else:
                    return self.export_excel(form)
        return render(request, 'home/form_error.html', {'form': form})

    def get_context_data(self, **kwargs):
        context = super(ConsultasPeriodo, self).get_context_data(**kwargs)
        context['base_template'] = get_vista_usuario(self.request)
        context['grafico'] = self.grafico
        return context

    def export_csv(self, form):
        estacion = form.cleaned_data['estacion']
        variable = form.cleaned_data['variable']
        fecha_inicio = form.cleaned_data['inicio']
        fecha_fin = form.cleaned_data['fin']
        if fecha_inicio is None:
            fecha_inicio = estacion.est_fecha_inicio
        if fecha_fin is None:
            fecha_fin = date.today()
        valores, maximos, minimos, tiempo = datos_instantaneos(estacion, variable, fecha_inicio, fecha_fin)
        # Establecemos el nombre del archivo
        nombre_archivo = str('"') + str(estacion.est_codigo) + str("_") + str(variable.var_nombre) + str('.csv"')
        contenido = "attachment; filename={0}".format(nombre_archivo)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = contenido
        writer = csv.writer(response)
        if variable.var_id == 1:
            writer.writerow(['fecha', 'valor'])
            for valor, fecha in zip(valores, tiempo):
                writer.writerow([fecha, valor])
        else:
            writer.writerow(['fecha', 'valor', 'maximo', 'minimo'])
            for valor, maximo, minimo, fecha in zip(valores, maximos, minimos, tiempo):
                writer.writerow([fecha, valor, maximo, minimo])

        return response

    def export_excel(self, form):
        return reporte_excel(form)


# consultas por periodo para usuarios invitados
class ConsultasUsuario(FormView):
    template_name = 'reportes/consultas_usuario.html'
    form_class = UsuarioSearchForm
    success_url = '/reportes/usuarios/'

    def post(self, request, *args, **kwargs):
        form = UsuarioSearchForm(self.request.POST or None)
        if form.is_valid():
            if self.request.is_ajax():
                datos = consultar_datos_usuario(form)
                return JsonResponse(datos, safe=False)
            else:
                return self.export_excel(form)
        return render(request, 'home/form_error.html', {'form': form})

    def get_context_data(self, **kwargs):
        context = super(ConsultasUsuario, self).get_context_data(**kwargs)
        return context

    @staticmethod
    def export_excel(form):
        return reporte_excel(form)


# consultas por periodo de todas las variables
class ConsultasEstacionVariable(FormView):
    template_name = 'reportes/consultas_estacion.html'
    form_class = EstacionVariableSearchForm
    success_url = '/reportes/estacionvariable'
    valores = []

    def post(self, request, *args, **kwargs):
        form = EstacionVariableSearchForm(self.request.POST or None)
        if form.is_valid():
            return self.export_csv(form)
        return render(request, 'home/form_error.html', {'form': form})

    def get_context_data(self, **kwargs):
        context = super(ConsultasEstacionVariable, self).get_context_data(**kwargs)
        return context

    @staticmethod
    def export_csv(form):
        estacion = form.cleaned_data['estacion']
        fecha_inicio = form.cleaned_data['inicio']
        fecha_fin = form.cleaned_data['fin']
        valores = datos_estacion(estacion, fecha_inicio, fecha_fin)
        # Establecemos el nombre del archivo
        nombre_archivo = str('"') + str(estacion.est_codigo) + str('.csv"')
        contenido = "attachment; filename={0}".format(nombre_archivo)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = contenido
        writer = csv.writer(response)
        num_col = len(valores)
        num_fil = len(valores[0])
        for i in range(num_fil):
            fila=[]
            for j in range(num_col):
                if i < len(valores[j]):
                    fila.append(valores[j][i])
                else:
                    fila.append('')
            writer.writerow(fila)
        return response


class ConsultaInamhi(FormView):
    template_name = 'reportes/consulta_inamhi.html'
    form_class = InamhiForm
    success_url = 'reportes/inamhi'

    def get_context_data(self, **kwargs):
        context = super(ConsultaInamhi, self).get_context_data(**kwargs)
        context['base_template'] = get_vista_usuario(self.request)
        return context

    def post(self, request, *args, **kwargs):
        form = InamhiForm(self.request.POST or None)
        informacion = dict(
            base_template=get_vista_usuario(request),
            form=form
        )
        if form.is_valid():
            grafico = procesar_json_inamhi(form)
            informacion.update(grafico)
            return render(request, 'reportes/consulta_inamhi.html', informacion)

        return render(request, 'reportes/consulta_inamhi.html', informacion)


class ConsultaDatos(TemplateView):
    template_name = 'reportes/mapa_estaciones.html'


# web service para consultar datos horarios
def datos_json_horarios(request, est_id, var_id, fec_ini, fec_fin):
    datos = datos_horarios_json(est_id, var_id, fec_ini, fec_fin)
    return JsonResponse(datos, safe=False)


# consultar variables de las estaciones del INAMHI
def variables_inamhi(request):
    estacion = request.GET.get('estacion', None)
    frecuencia = request.GET.get('frecuencia', None)
    inamhi = Inamhi.objects.get(id=estacion)
    parametros = Parametro.objects.filter(frecuencia=frecuencia, tipo=inamhi.categoria)
    lista = {}
    for item in parametros:
        lista[item.id] = item.nombre + ' ' + item.estadistico

    return JsonResponse(lista)


def get_vista_usuario(request):
    if request.user.is_authenticated:
        template = "index.html"
    else:
        template = "index_invitado.html"
    return template
