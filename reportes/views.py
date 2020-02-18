from estacion.models import Inamhi, Estacion, Sistema, Cuenca, SistemaCuenca
from variable.models import Parametro, Variable
from cruce.models import Cruce

from django.views.generic import FormView, TemplateView
from reportes.forms import AnuarioForm, InamhiForm
from reportes.consultas.forms import (MedicionSearchForm, ComparacionForm, VariableForm,
                                      EstacionVariableSearchForm, UsuarioSearchForm, ConsultasForm)
import csv

from reportes.consultas.functions import (
    datos_horarios_json,
    datos_instantaneos,
    datos_estacion,
    reporte_excel
)
from reportes.functions import (filtrar, comparar, comparar_variables, procesar_json_inamhi,
                                consultar_datos_usuario)
from reportes.excel import reporte_excel_anuario

from reportes.sistemacuenca import (
    get_datos_graficar,
    export_csv,
    export_excel
)

from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import date, datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q, Prefetch
import requests


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
            print(request.POST)
            if request.POST.get('grafico') == '':
                self.lista = filtrar(form)
                context.update(self.lista)
                context['base_template'] = get_vista_usuario(self.request)
                return render(request, 'reportes/anuario_normal.html', context)
            else:
                return reporte_excel_anuario(form)

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

                datos = consultar_datos_usuario(form)
                return JsonResponse(datos, safe=False)
            else:
                '''if 'graficar' in request.POST:
                    context = super(ConsultasPeriodo, self).get_context_data(**kwargs)
                    context.update(consultar_datos(form))
                    context['base_template'] = get_vista_usuario(self.request)
                    return render(request, 'reportes/consultas_periodo.html', context)'''

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
        informacion = datos_instantaneos(estacion, variable, fecha_inicio, fecha_fin)
        valores=informacion['valor']
        maximos = informacion['max_abs']
        minimos = informacion['min_abs']
        tiempo = informacion['tiempo']
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

    @staticmethod
    def export_excel(form):
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


# Consultas Estacion Sistema Cuenca
class ConsultasSistema(LoginRequiredMixin, FormView):
    template_name = 'reportes/consultas_sistema.html'
    form_class = ConsultasForm
    success_url = '/reportes/sistema'

    def post(self, request, *args, **kwargs):
        form = ConsultasForm(self.request.POST or None)
        if form.is_valid():
            variable = form.cleaned_data['variable']
            estacion = form.cleaned_data['estacion']
            inicio = form.cleaned_data['inicio']
            fin = form.cleaned_data['fin']
            frecuencia = form.data["frecuencia"]

            if self.request.is_ajax():
                datos = get_datos_graficar(estacion, variable, inicio, fin, frecuencia, None)
                # graf1 = grafico(datos, variable, estacion, titulo)
                #return render(request, 'reportes/consultas/porPeriodo.html', {'grafico': graf1})
                return JsonResponse(datos, safe=False)
            else:
                if 'accion' not in request.POST:
                    return
                if request.POST['accion'] == 'csv':
                    response = export_csv(estacion, variable, inicio, fin, frecuencia, None)
                    if response: return response
                    form.mensaje = "No hay datos (" + frecuencia + ") en estación " + \
                                   estacion.est_codigo + " en " + variable.var_nombre + " en el período seleccionado."
                    return self.render_to_response(self.get_context_data(form=form))
                elif request.POST['accion'] == 'excel':
                    response = export_excel(estacion, variable, inicio, fin, frecuencia, None)
                    if response: return response
                    form.mensaje = "No hay datos (" + frecuencia + ") en estación " + \
                                   estacion.est_codigo + " en " + variable.var_nombre + " en el período seleccionado."
                    return self.render_to_response(self.get_context_data(form=form))

        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(ConsultasSistema, self).get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super(ConsultasSistema, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


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
            if self.request.is_ajax():
                datos = procesar_json_inamhi(form)
                return JsonResponse(datos, safe=False)
            else:
                return self.export_csv(form)

            grafico = procesar_json_inamhi(form)
            informacion.update(grafico)
            return render(request, 'reportes/consulta_inamhi.html', informacion)

        return render(request, 'reportes/consulta_inamhi.html', informacion)

    @staticmethod
    def export_csv(form):
        estacion = form.cleaned_data['estacion']
        parametro = form.cleaned_data['parametro']
        frecuencia = form.cleaned_data['frecuencia']
        inicio = form.cleaned_data['inicio']
        fin = form.cleaned_data['fin']

        fecha_inicio = datetime(inicio.year, inicio.month, inicio.day, 0, 0, 0)
        fecha_fin = datetime(fin.year, fin.month, fin.day, 23, 59, 59, 999999)
        # formato url web service INAMHI
        url_base = 'http://186.42.174.236:8090/'
        url_base += frecuencia + '/'
        url_base += str(estacion.identificador) + '/'
        url_base += fecha_inicio.strftime("%Y-%m-%d %H:%M:%S") + '/'
        url_base += fecha_fin.strftime("%Y-%m-%d %H:%M:%S") + '/'
        url_base += estacion.transmision + '/'
        url_base += parametro.parametro

        response = requests.get(url_base, auth=('FONAG', 'fOnAg2018'))
        data = response.json()
        tiempo = []
        valores = []
        if len(data) > 0:
            # print(data)
            for item in data:
                fecha = datetime.strptime(item['fechaTomaDelDato'], '%Y-%m-%d %H:%M:%S')

                if len(item['dataJSON']) > 0:

                    if item['dataJSON'][0]['valor'] is not None:
                        valores.append(item['dataJSON'][0]['valor'])
                        tiempo.append(fecha)
                else:
                    valores.append(None)


        # Establecemos el nombre del archivo
        nombre_archivo = str('"') + str(estacion) + str("_") + str(parametro) + str('.csv"')
        contenido = "attachment; filename={0}".format(nombre_archivo)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = contenido
        writer = csv.writer(response)

        writer.writerow(['fecha', 'valor'])
        for valor, fecha in zip(valores, tiempo):
            writer.writerow([fecha, valor])
        return response


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


# consultar estaciones por tipo de trasnmision
def tipo_estaciones(request):
    transmision = request.GET.get('transmision', None)
    if transmision == str(0):
        estaciones = Estacion.objects.all()
    elif transmision == str(1):
        estaciones = Estacion.objects.filter(transmision=True)
    else:
        estaciones = Estacion.objects.filter(transmision=False)
    lista = {}

    for item in estaciones:
        lista[item.est_id] = item.est_codigo
    return JsonResponse(lista)

# @login_required
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


# @login_required
def cuencas(request):
    try:
        sistema_id = int(request.GET.get('sistema_id', None))
    except ValueError:
        sistema_id = None
    if sistema_id is not None:
        cuencas = SistemaCuenca.objects.prefetch_related(
            Prefetch('cuenca', queryset=Cuenca.objects.all())
        ).filter(sistema_id=sistema_id)
    else:
        cuencas = SistemaCuenca.objects.all()
    lista = {}
    for row in cuencas:
        try:
            lista[row.cuenca.id] = row.cuenca.nombre
        except:
            pass
    return JsonResponse(lista)


# @login_required
def estaciones(request):
    variable_id = sistema_id = cuenca_id = estacion_tipo_id = unidadoperativa_id = None
    filtro = Q()

    try:
        variable_id = int(request.GET.get('variable_id', None))
    except Exception as e:
        pass

    try:
        sistema_id = int(request.GET.get('sistema_id', None))
    except Exception as e:
        pass

    try:
        cuenca_id = int(request.GET.get('cuenca_id', None))
    except Exception as e:
        pass

    try:
        estacion_tipo_id = int(request.GET.get('estacion_tipo_id', None))
    except Exception as e:
        pass

    try:
        unidadoperativa_id = int(request.GET.get('unidadoperativa_id', None))
    except Exception as e:
        pass

    if variable_id:
        filtro &= Q(cruce__var_id_id=variable_id)
    if sistema_id:
        filtro &= Q(sistemacuenca__sistema_id=sistema_id)
    if cuenca_id:
        filtro &= Q(sistemacuenca__cuenca_id=cuenca_id)
    if estacion_tipo_id:
        filtro &= Q(tipo_id=estacion_tipo_id)


    estaciones = Estacion.objects.filter(filtro)

    imagen=None
    if cuenca_id:
        imagen = Cuenca.objects.get(id=cuenca_id).imagen
    elif sistema_id:
        imagen = Sistema.objects.get(id=sistema_id).imagen

    try:
        imagen_url = imagen.url
    except:
        imagen_url = ""

    lista = {'estaciones':{}, 'imagen': imagen_url}

    for row in estaciones:
        lista['estaciones'][row.est_id] = row.est_codigo + " - " + row.est_nombre
    return JsonResponse(lista)


def get_vista_usuario(request):
    if request.user.is_authenticated:
        template = "index.html"
    else:
        template = "index_invitado.html"
    return template
