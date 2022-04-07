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

import csv
from datetime import date, datetime

import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import FormView, TemplateView

from anuarios import functions as funanuario
from cruce.models import Cruce

# from estacion.models import Inamhi, Estacion, Sitio, Cuenca, SitioCuenca
from estacion.models import Cuenca, Estacion, Sitio, SitioCuenca
from home.views import AjaxableResponseMixin
from reportes_v2.consultas.forms import (
    ComparacionForm,
    ComparacionFormPublico,
    ConsultasForm,
    ConsultasPeriodoForm,
    EstacionVariableSearchForm,
    UsuarioSearchForm,
    VariableForm,
    VariableFormPublico,
)
from reportes_v2.consultas.functions import (
    datos_estacion,
    datos_horarios_json,
    datos_instantaneos,
    reporte_csv,
    reporte_excel,
)
from reportes_v2.excel import reporte_excel_anuario
from reportes_v2.forms import AnuarioForm
from reportes_v2.functions import (
    comparar,
    comparar_variables,
    consultar_datos_usuario,
    filtrar,
    mapa_estaciones_variable,
    procesar_json_inamhi,
)
from reportes_v2.sitiocuenca import export_csv, export_excel, get_datos_graficar
from variable.models import Variable


class reportes_v2Anuario(FormView):
    template_name = "reportes_v2/anuario_normal.html"
    form_class = AnuarioForm
    success_url = "/reportes_v2/anuario/"
    lista = {}

    def get_context_data(self, **kwargs):
        context = super(reportes_v2Anuario, self).get_context_data(**kwargs)
        context["base_template"] = get_vista_usuario(self.request)
        return context

    def post(self, request, *args, **kwargs):
        form = AnuarioForm(self.request.POST or None)
        if form.is_valid():
            context = super(reportes_v2Anuario, self).get_context_data(**kwargs)
            print(request.POST)
            var = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            # var = [1,2,3,4,5,6,7,8,9,11]
            estacion = form.cleaned_data["estacion"]
            periodo = form.cleaned_data["anio"]
            for item in var:
                exists = funanuario.verficar_anuario(estacion, item, periodo)
                if exists == False:
                    datos = funanuario.calcular(estacion, item, periodo)
                    template = funanuario.template(item)
                    funanuario.guardar_variable(datos, estacion, item, periodo)
            if request.POST.get("grafico") == "":
                self.lista = filtrar(estacion, periodo)
                context.update(self.lista)
                context["base_template"] = get_vista_usuario(self.request)
                return render(request, "reportes_v2/anuario_normal.html", context)
            else:
                return reporte_excel_anuario(estacion, periodo)

        return render(
            request,
            self.template_name,
            {"form": form, "mensaje": "Formulario inválido."},
        )


# vista para comparar tres estaciones una sola variable
class ComparacionValores(LoginRequiredMixin, AjaxableResponseMixin, FormView):
    template_name = "reportes_v2/comparacion_reporte.html"
    form_class = ComparacionForm
    success_url = "/reportes_v2/comparacion/"
    grafico = []

    def get_context_data(self, **kwargs):
        context = super(ComparacionValores, self).get_context_data(**kwargs)
        context["base_template"] = "index.html"
        return context

    def post(self, request, *args, **kwargs):
        form = ComparacionForm(self.request.POST or None)
        if form.is_valid() and self.request.is_ajax():
            diccionario = comparar(form)
            return JsonResponse(diccionario, safe=False)

        # return render(request, 'home/form_error.html', {'form': form})
        return JsonResponse({"resultado": False})


# Vista para comparar estaciones por una variable para el público
class CompararEstacionesPublico(AjaxableResponseMixin, FormView):
    template_name = "reportes_v2/comparacion_reporte.html"
    form_class = ComparacionFormPublico
    success_url = "/reportes_v2/comparacion/"
    grafico = []

    def get_context_data(self, **kwargs):
        context = super(CompararEstacionesPublico, self).get_context_data(**kwargs)
        context["base_template"] = get_vista_usuario(self.request)
        return context

    def post(self, request, *args, **kwargs):
        form = ComparacionFormPublico(self.request.POST or None)
        if form.is_valid() and self.request.is_ajax():
            diccionario = comparar(form)
            lista = {"resultado": True}
            return JsonResponse(diccionario, safe=False)
        # return render(request, 'home/form_error.html', {'form': form})
        return JsonResponse({"resultado": False})


class MapaCompararEstaciones(FormView):
    form_class = ComparacionForm

    def get(self, request, *args, **kwargs):
        var_id = kwargs.get("var_id")
        if request.user.is_authenticated:
            diccionario = mapa_estaciones_variable(var_id, True)
        else:
            diccionario = mapa_estaciones_variable(var_id, False)
        return JsonResponse(diccionario)


class MapaCompararEstacionesPublico(FormView):
    form_class = ComparacionForm

    def get(self, request, *args, **kwargs):
        var_id = kwargs.get("var_id")
        diccionario = mapa_estaciones_variable(var_id, False)
        return JsonResponse(diccionario)


# vista para comparar 2 estaciones y dos Variables
class ComparacionVariables(LoginRequiredMixin, FormView):
    template_name = "reportes_v2/comparacion_variable.html"
    form_class = VariableForm
    success_url = "/reportes_v2/compararvariable/"
    grafico = []

    def get_context_data(self, **kwargs):
        context = super(ComparacionVariables, self).get_context_data(**kwargs)

        context["base_template"] = "index.html"
        return context

    def post(self, request, *args, **kwargs):
        form = VariableForm(self.request.POST or None)
        if form.is_valid() and self.request.is_ajax():
            """self.grafico = comparar_variable(form)
            plantilla = 'reportes_v2/consultas/grafico.html'
            diccionario = {'grafico': self.grafico}
            return render(request, plantilla, diccionario)"""
            datos = comparar_variables(form)
            return JsonResponse(datos, safe=False)
        return render(request, "home/form_error.html", {"form": form})


# vista para comparar 2 estaciones y dos Variables
class ComparacionVariablesPublico(FormView):
    template_name = "reportes_v2/comparacion_variable.html"
    form_class = VariableFormPublico
    success_url = "/reportes_v2/compararvariable/"
    grafico = []

    def get_context_data(self, **kwargs):
        context = super(ComparacionVariablesPublico, self).get_context_data(**kwargs)
        context["base_template"] = get_vista_usuario(self.request)
        return context

    def post(self, request, *args, **kwargs):
        form = VariableForm(self.request.POST or None)
        if form.is_valid() and self.request.is_ajax():
            datos = comparar_variables(form)
            return JsonResponse(datos, safe=False)
        return render(request, "home/form_error.html", {"form": form})


# consultas por periodo y frecuencia horaria, diaria y mensual
class ConsultasPeriodo(FormView):
    template_name = "reportes_v2/consultas_periodo.html"
    form_class = ConsultasPeriodoForm
    success_url = "/reportes_v2/consultas"
    frecuencia = str("")
    valores = []
    grafico = []

    def post(self, request, *args, **kwargs):
        form = ConsultasPeriodoForm(self.request.POST or None)
        if form.is_valid():
            self.frecuencia = form.cleaned_data["frecuencia"]
            if self.request.is_ajax():
                datos = consultar_datos_usuario(form)
                return JsonResponse(datos, safe=False)
            else:
                if self.frecuencia == "0":
                    return self.export_csv(form)
                else:
                    return self.export_excel(form)
        return render(request, "home/form_error.html", {"form": form})

    def get_context_data(self, **kwargs):
        context = super(ConsultasPeriodo, self).get_context_data(**kwargs)
        context["base_template"] = get_vista_usuario(self.request)
        context["grafico"] = self.grafico
        return context

    def export_csv(self, form):
        estacion = form.cleaned_data["estacion"]
        variable = form.cleaned_data["variable"]
        fecha_inicio = form.cleaned_data["inicio"]
        fecha_fin = form.cleaned_data["fin"]
        if fecha_inicio is None:
            fecha_inicio = estacion.est_fecha_inicio
        if fecha_fin is None:
            fecha_fin = date.today()
        informacion = datos_instantaneos(estacion, variable, fecha_inicio, fecha_fin)
        valores = informacion["valor"]
        maximos = informacion["max_abs"]
        minimos = informacion["min_abs"]
        tiempo = informacion["tiempo"]
        # Establecemos el nombre del archivo
        nombre_archivo = (
            str('"')
            + str(estacion.est_codigo)
            + str("_")
            + str(variable.var_nombre)
            + str('.csv"')
        )
        contenido = "attachment; filename={0}".format(nombre_archivo)
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = contenido
        writer = csv.writer(response)
        if variable.var_id == 1:
            writer.writerow(["fecha", "valor"])
            for valor, fecha in zip(valores, tiempo):
                writer.writerow([fecha, valor])
        else:
            writer.writerow(["fecha", "valor", "maximo", "minimo"])
            for valor, maximo, minimo, fecha in zip(valores, maximos, minimos, tiempo):
                writer.writerow([fecha, valor, maximo, minimo])

        return response

    @staticmethod
    def export_excel(form):
        return reporte_excel(form)

    def get_form_kwargs(self):
        kwargs = super(ConsultasPeriodo, self).get_form_kwargs()
        kwargs.update({"is_authenticated": self.request.user.is_authenticated})
        return kwargs


# consultas por periodo para usuarios invitados
class ConsultasUsuario(FormView):
    template_name = "reportes_v2/consultas_usuario.html"
    form_class = UsuarioSearchForm
    # form_class = MedicionSearchForm
    success_url = "/reportes_v2/usuarios/"
    frecuencia = str("")

    def post(self, request, *args, **kwargs):
        form = UsuarioSearchForm(self.request.POST or None)
        if form.is_valid():
            self.frecuencia = form.cleaned_data["frecuencia"]
            if self.request.is_ajax():
                datos = consultar_datos_usuario(form)
                return JsonResponse(datos, safe=False)
            else:
                if self.frecuencia == "0":
                    return self.export_csv(form)
                else:
                    return self.export_excel(form)
        return render(request, "home/form_error.html", {"form": form})

    def get_context_data(self, **kwargs):
        context = super(ConsultasUsuario, self).get_context_data(**kwargs)
        return context

    @staticmethod
    def export_csv(form):
        return reporte_csv(form)

    @staticmethod
    def export_excel(form):
        return reporte_excel(form)


# Consultas Estacion Sitio Cuenca
class ConsultasSitio(LoginRequiredMixin, FormView):
    template_name = "reportes_v2/consultas_sitio.html"
    form_class = ConsultasForm
    success_url = "/reportes_v2/sitio"

    def post(self, request, *args, **kwargs):
        form = ConsultasForm(self.request.POST or None)
        if form.is_valid():
            variable = form.cleaned_data["variable"]
            estacion = form.cleaned_data["estacion"]
            inicio = form.cleaned_data["inicio"]
            fin = form.cleaned_data["fin"]
            frecuencia = form.data["frecuencia"]

            if self.request.is_ajax():
                datos = get_datos_graficar(
                    estacion, variable, inicio, fin, frecuencia, None
                )
                # graf1 = grafico(datos, variable, estacion, titulo)
                # return render(request, 'reportes_v2/consultas/porPeriodo.html', {'grafico': graf1})
                return JsonResponse(datos, safe=False)
            else:
                if "accion" not in request.POST:
                    return
                if request.POST["accion"] == "csv":
                    response = export_csv(
                        estacion, variable, inicio, fin, frecuencia, None
                    )
                    if response:
                        return response
                    form.mensaje = (
                        "No hay datos ("
                        + frecuencia
                        + ") en estación "
                        + estacion.est_codigo
                        + " en "
                        + variable.var_nombre
                        + " en el período seleccionado."
                    )
                    return self.render_to_response(self.get_context_data(form=form))
                elif request.POST["accion"] == "excel":
                    response = export_excel(
                        estacion, variable, inicio, fin, frecuencia, None
                    )
                    if response:
                        return response
                    form.mensaje = (
                        "No hay datos ("
                        + frecuencia
                        + ") en estación "
                        + estacion.est_codigo
                        + " en "
                        + variable.var_nombre
                        + " en el período seleccionado."
                    )
                    return self.render_to_response(self.get_context_data(form=form))

        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(ConsultasSitio, self).get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super(ConsultasSitio, self).get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


# consultas por periodo de todas las variables
class ConsultasEstacionVariable(FormView):
    template_name = "reportes_v2/consultas_estacion.html"
    form_class = EstacionVariableSearchForm
    success_url = "/reportes_v2/estacionvariable"
    valores = []

    def post(self, request, *args, **kwargs):
        form = EstacionVariableSearchForm(self.request.POST or None)
        if form.is_valid():
            return self.export_csv(form)
        return render(request, "home/form_error.html", {"form": form})

    def get_context_data(self, **kwargs):
        context = super(ConsultasEstacionVariable, self).get_context_data(**kwargs)
        return context

    @staticmethod
    def export_csv(form):
        estacion = form.cleaned_data["estacion"]
        fecha_inicio = form.cleaned_data["inicio"]
        fecha_fin = form.cleaned_data["fin"]
        valores = datos_estacion(estacion, fecha_inicio, fecha_fin)
        # Establecemos el nombre del archivo
        nombre_archivo = str('"') + str(estacion.est_codigo) + str('.csv"')
        contenido = "attachment; filename={0}".format(nombre_archivo)
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = contenido
        writer = csv.writer(response)
        num_col = len(valores)
        num_fil = len(valores[0])
        for i in range(num_fil):
            fila = []
            for j in range(num_col):
                if i < len(valores[j]):
                    fila.append(valores[j][i])
                else:
                    fila.append("")
            writer.writerow(fila)
        return response


class ConsultaDatos(TemplateView):
    template_name = "reportes_v2/mapa_estaciones.html"


# web service para consultar datos horarios
def datos_json_horarios(request, est_id, var_id, fec_ini, fec_fin):
    datos = datos_horarios_json(est_id, var_id, fec_ini, fec_fin)
    return JsonResponse(datos, safe=False)


# # consultar variables de las estaciones del INAMHI
# def variables_inamhi(request):
#     estacion = request.GET.get('estacion', None)
#     frecuencia = request.GET.get('frecuencia', None)
#     inamhi = Inamhi.objects.get(id=estacion)
#     parametros = Parametro.objects.filter(frecuencia=frecuencia, tipo=inamhi.categoria)
#     lista = {}
#     for item in parametros:
#         lista[item.id] = item.nombre + ' ' + item.estadistico
#
#     return JsonResponse(lista)


# consultar estaciones por tipo de trasnmision
def tipo_estaciones(request):
    transmision = request.GET.get("transmision", None)
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


# Lista de Variables por Estación @login_required
def variables(request):
    try:
        estacion_id = int(request.GET.get("estacion_id", None))
    except ValueError:
        estacion_id = None

    lista = {}
    if estacion_id is not None:
        variables = Cruce.objects.prefetch_related(
            Prefetch("var_id", queryset=Variable.objects.all())
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
        sitio_id = int(request.GET.get("sitio_id", None))
    except ValueError:
        sitio_id = None
    if sitio_id is not None:
        cuencas = SitioCuenca.objects.prefetch_related(
            Prefetch("cuenca", queryset=Cuenca.objects.all())
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


# @login_required
def estaciones(request):
    variable_id = sitio_id = cuenca_id = estacion_tipo_id = unidadoperativa_id = None
    filtro = Q()

    try:
        variable_id = int(request.GET.get("variable_id", None))
    except Exception as e:
        pass

    try:
        sitio_id = int(request.GET.get("sitio_id", None))
    except Exception as e:
        pass

    try:
        cuenca_id = int(request.GET.get("cuenca_id", None))
    except Exception as e:
        pass

    try:
        estacion_tipo_id = int(request.GET.get("estacion_tipo_id", None))
    except Exception as e:
        pass

    try:
        unidadoperativa_id = int(request.GET.get("unidadoperativa_id", None))
    except Exception as e:
        pass

    if variable_id:
        filtro &= Q(cruce__var_id_id=variable_id)
    if sitio_id:
        filtro &= Q(sitiocuenca__sitio_id=sitio_id)
    if cuenca_id:
        filtro &= Q(sitiocuenca__cuenca_id=cuenca_id)
    if estacion_tipo_id:
        filtro &= Q(tipo_id=estacion_tipo_id)

    estaciones = Estacion.objects.filter(filtro)

    imagen = None

    if cuenca_id:
        imagen = Cuenca.objects.get(id=cuenca_id).imagen
    elif sitio_id:
        imagen = Sitio.objects.get(id=sitio_id).imagen

    try:
        imagen_url = imagen.url
    except:
        imagen_url = ""

    lista = {"estaciones": {}, "imagen": imagen_url}

    for row in estaciones:
        lista["estaciones"][row.est_id] = row.est_codigo + " - " + row.est_nombre
    return JsonResponse(lista)


def get_vista_usuario(request):
    if request.user.is_authenticated:
        template = "index.html"
    else:
        template = "index_invitado.html"
    return template
