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

import json
from datetime import datetime, time

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
from django.db.models import Max, Min
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import FormView, ListView

from estacion.views import listar_anio
from medicion.forms import ValidationSearchForm
from medicion.models import *
from reportes import functions as functions1
from validacion import functions as funcvariable
from validacion_v2 import functions
from validacion_v2.forms import BorrarForm
from variable.models import Variable


# Create your views here.
# Consulta de datos diarios por reporte
class ValidacionDiaria(LoginRequiredMixin, FormView):
    template_name = "validacion_v2/validacion_diaria.html"
    form_class = ValidationSearchForm
    success_url = "/validacion_v2/diaria/"

    def post(self, request, *args, **kwargs):
        form = ValidationSearchForm(self.request.POST or None)
        if form.is_valid():
            if self.request.is_ajax():
                modelo = "Var" + form.data["variable"] + "Medicion"
                modelo = globals()[modelo]
                fechaa = modelo.objects.filter(
                    estacion_id__exact=form.data["estacion"]
                ).aggregate(Max("fecha"), Min("fecha"))

                if form.data["inicio"] == "":
                    inicio = fechaa["fecha__min"]
                else:
                    inicio = datetime.combine(
                        form.cleaned_data["inicio"], time(0, 0, 0, 0)
                    )

                if form.data["fin"] == "":
                    fin = fechaa["fecha__max"]
                    fin = datetime.combine(fin, time(23, 59, 59, 999999))
                else:
                    fin = datetime.combine(
                        form.cleaned_data["fin"], time(23, 59, 59, 999999)
                    )
                variable = form.cleaned_data["variable"]
                estacion = form.cleaned_data["estacion"]
                if form.data["variable"] == "5" or form.data["variable"] == "4":
                    lista = funcvariable.reporte_validacion(form)
                    _grafico = funcvariable.grafico2(lista, variable, estacion)
                else:
                    # lista = functions.reporte_validacion(form,inicio,fin)
                    # _grafico = functions.grafico(lista, variable,  estacion,inicio,fin)
                    consulta = functions1.consulta_crudos(
                        estacion.est_id, variable.var_id, inicio, fin
                    )
                    data = []
                    for row in consulta:
                        data.append([row.fecha, row.valor])

                # _grafico = functions.grafico(lista, variable,  estacion,inicio,fin)
                maximo = form.cleaned_data["limite_superior"]
                minimo = form.cleaned_data["limite_inferior"]
                # data = functions.reporte_diario(estacion, variable, inicio, fin, maximo, minimo)
                # if type(_grafico) == type('str'):
                #     pass
                # else:
                #     _grafico = 'No Hay Datos'
                lista = functions.reporte_diario(
                    estacion, variable, inicio, fin, maximo, minimo, data
                )
                lista_json = json.dumps(lista, allow_nan=True, cls=DjangoJSONEncoder)
                # return JsonResponse(data, safe=False)
                return HttpResponse(lista_json, content_type="application/json")

        # return self.render_to_response(self.get_context_data(form=form))
        return render(request, "home/form_error.html", {"form": form})


# Consulta de datos crudos y/o validados por estacion, variable y hora
class ListaValidacion(LoginRequiredMixin, ListView):
    template_name = "home/mensaje.html"

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            est_id = kwargs.get("estacion")
            var_id = kwargs.get("variable")
            fecha_str = kwargs.get("fecha")
            maximo = kwargs.get("maximo")
            minimo = kwargs.get("minimo")

            datos = functions.consultar_diario(
                est_id, var_id, fecha_str, maximo, minimo
            )
            data_json = json.dumps(datos, allow_nan=True, cls=DjangoJSONEncoder)
            return HttpResponse(data_json, content_type="application/json")
        mensaje = "Ocurrio un problema con el procesamiento de la información, por favor contacte con el administrador"
        return render(request, "home/mensaje.html", {"mensaje": mensaje})


# Consular los periodos de validacion por estacion y variable
class PeriodosValidacion(LoginRequiredMixin, FormView):
    template_name = "validacion_v2/periodos_validacion.html"
    form_class = ValidationSearchForm
    success_url = "/medicion/filter/"
    lista = []

    def post(self, request, *args, **kwargs):
        estacion_id = None
        variable_id = None
        try:
            estacion_id = int(request.POST.get("estacion", None))
            variable_id = int(request.POST.get("variable", None))
            print(estacion_id)
            inicio = request.POST.get("inicio", None)
            variable = Variable.objects.get(var_id=variable_id)
            modelo = variable.var_modelo.lower()
        except:
            pass

        intervalos = functions.periodos_validacion(
            est_id=estacion_id, variable=variable, inicio=inicio
        )
        return render(request, self.template_name, {"intervalos": intervalos})


class ValidacionBorrar(LoginRequiredMixin, FormView):
    template_name = "validacion/borrar.html"
    form_class = BorrarForm
    success_url = "/validacion/borrar/"
    resultado = None

    def form_valid(self, form):
        estacion_id = form.cleaned_data["estacion"].est_id
        var_id = form.cleaned_data["variable"].var_id
        inicio = form.cleaned_data["inicio"]
        fin = form.cleaned_data["fin"]

        filas_validado = 0
        sql = "DELETE FROM validacion_var%%var_id%%validado WHERE estacion_id = %s AND fecha >= %s AND fecha <= %s;"
        if variable.var_id == 4 or variable.var_id == 5:
            sql = """DELETE FROM validacion_viento WHERE estacion_id = %s AND fecha >= %s AND fecha <= %s;
            DELETE FROM validacion_var4validado WHERE estacion_id = %s AND fecha >= %s AND fecha <= %s;
            DELETE FROM validacion_var5validado WHERE estacion_id = %s AND fecha >= %s AND fecha <= %s;
            """

        sql = sql.replace("%%var_id%%", str(var_id))
        with connection.cursor() as cursor:
            cursor.execute(sql, [estacion_id, inicio, fin])
            filas_validado = cursor.rowcount

        filas_horario = 0
        sql = "DELETE FROM horario_var%%var_id%%horario WHERE estacion_id = %s AND fecha >= date_trunc('hour', %s) AND fecha <= date_trunc('hour', %s);"
        if variable.var_id == 4 or variable.var_id == 5:
            sql = """DELETE FROM horario_var4horario WHERE estacion_id = %s AND fecha >= date_trunc('hour', %s) AND fecha <= date_trunc('hour', %s);
            DELETE FROM horario_var5horario WHERE estacion_id = %s AND fecha >= date_trunc('hour', %s) AND fecha <= date_trunc('hour', %s);"""

        sql = sql.replace("%%var_id%%", str(var_id))
        with connection.cursor() as cursor:
            cursor.execute(sql, [estacion_id, inicio, fin])
            filas_horario = cursor.rowcount

        filas_diario = 0
        sql = "DELETE FROM diario_var%%var_id%%diario WHERE estacion_id = %s AND fecha >= date_trunc('day', %s) AND fecha <= date_trunc('day', %s);"
        if variable.var_id == 4 or variable.var_id == 5:
            sql = """DELETE FROM diario_var4diario WHERE estacion_id = %s AND fecha >= date_trunc('hour', %s) AND fecha <= date_trunc('hour', %s);
            DELETE FROM diario_var5diario WHERE estacion_id = %s AND fecha >= date_trunc('hour', %s) AND fecha <= date_trunc('hour', %s);"""

        sql = sql.replace("%%var_id%%", str(var_id))
        with connection.cursor() as cursor:
            cursor.execute(sql, [estacion_id, inicio, fin])
            filas_diario = cursor.rowcount

        filas_mensual = 0
        sql = "DELETE FROM mensual_var%%var_id%%mensual WHERE estacion_id = %s AND fecha >= date_trunc('month', %s) AND fecha <= date_trunc('month', %s);"
        if variable.var_id == 4 or variable.var_id == 5:
            sql = """DELETE FROM mensual_var4mensual WHERE estacion_id = %s AND fecha >= date_trunc('hour', %s) AND fecha <= date_trunc('hour', %s);
            DELETE FROM mensual_var5mensual WHERE estacion_id = %s AND fecha >= date_trunc('hour', %s) AND fecha <= date_trunc('hour', %s);"""

        sql = sql.replace("%%var_id%%", str(var_id))
        with connection.cursor() as cursor:
            cursor.execute(sql, [estacion_id, inicio, fin])
            filas_mensual = cursor.rowcount

        if self.request.is_ajax():
            data = {
                "filas_validado": filas_validado,
                "filas_horario": filas_horario,
                "filas_diario": filas_diario,
                "filas_mensual": filas_mensual,
            }
            cursor.close()
            return JsonResponse(data)
        else:
            cursor.close()
            return super().form_valid(form)


def guardar_crudos(request):
    # Verificando datos json para evitar inyeccion SQL
    estacion_id = int(request.POST.get("estacion_id", None))
    variable_id = int(request.POST.get("variable_id", None))
    cambios_json = request.POST.get("cambios", None)
    print("Guardar Crudos")
    variable = Variable.objects.get(var_id=variable_id)
    variable_nombre = str(variable_id)
    cambios_lista = json.loads(cambios_json)

    # print(cambios_json)

    fecha_inicio_dato = cambios_lista[0]["fecha"]
    fecha_fin_dato = cambios_lista[-1]["fecha"]
    # Borrar datos
    if variable.var_id == 4 or variable.var_id == 5:
        with connection.cursor() as cursor:
            sql = """DELETE FROM validacion_viento WHERE estacion_id = %s AND fecha >= %s AND fecha <= %s;
            """
            cursor.execute(sql, [estacion_id, fecha_inicio_dato, fecha_fin_dato])
            sql = """DELETE FROM validacion_var4validado WHERE estacion_id = %s AND fecha >= %s AND fecha <= %s;
            """
            cursor.execute(sql, [estacion_id, fecha_inicio_dato, fecha_fin_dato])
            sql = """DELETE FROM validacion_var5validado WHERE estacion_id = %s AND fecha >= %s AND fecha <= %s;
            """
            cursor.execute(sql, [estacion_id, fecha_inicio_dato, fecha_fin_dato])
        cursor.close()
    # elif variable.var_id == 10 or variable.var_id == 11:
    #    with connection.cursor() as cursor:
    #        sql = "DELETE FROM validacion_agua WHERE estacion_id = %s AND fecha >= %s AND fecha <= %s;"
    #        cursor.execute(sql, [estacion_id, fecha_inicio_dato, fecha_fin_dato])
    #    cursor.close()
    else:
        with connection.cursor() as cursor:
            sql = "DELETE FROM validacion_var%%var_id%%validado WHERE estacion_id = %s AND fecha >= %s AND fecha <= %s;"
            sql = sql.replace("%%var_id%%", str(variable_nombre))
            print(sql)
            cursor.execute(sql, [estacion_id, fecha_inicio_dato, fecha_fin_dato])
        cursor.close()
    if variable.var_id == 4 or variable.var_id == 5:
        with connection.cursor() as cursor:
            cursor.callproc("insertar_viento_validacion", [estacion_id, cambios_json])
            resultado = cursor.fetchone()[0]
        cursor.close()
    # elif variable.var_id == 10 or variable.var_id == 11:
    #    with connection.cursor() as cursor:
    #        cursor.callproc('insertar_agua_validacion', [estacion_id, cambios_json])
    #        resultado = cursor.fetchone()[0]
    #    cursor.close()
    else:
        with connection.cursor() as cursor:
            modelo = functions.normalize(variable.var_nombre).replace(" de ", "")
            modelo = modelo.replace(" ", "")
            variable_nombre = str(modelo)
            cursor.callproc(
                "insertar_" + variable_nombre.lower() + "_validacion",
                [estacion_id, cambios_json],
            )
            resultado = cursor.fetchone()[0]
            print(resultado)
        cursor.close()

    if resultado:
        lista = {"resultado": resultado}

    else:
        lista = {"resultado": False}
    print(resultado)
    return JsonResponse(lista)


# Pasar los datos crudos a validados
def guardar_validados(request):
    # Verificando datos json para evitar inyeccion SQL
    estacion_id = int(request.POST.get("estacion_id", None))
    variable_id = int(request.POST.get("variable_id", None))
    limite_superior = float(request.POST.get("limite_superior", None))
    limite_inferior = float(request.POST.get("limite_inferior", None))
    cambios_json = request.POST.get("cambios", None)

    variable = Variable.objects.get(var_id=variable_id)
    cambios_lista = json.loads(cambios_json)

    condiciones = functions.get_condiciones(cambios_lista)

    resultado = functions.pasar_crudos_validados(
        cambios_lista,
        variable,
        estacion_id,
        condiciones,
        limite_superior,
        limite_inferior,
    )

    if resultado:
        lista = {"resultado": resultado}
    else:
        lista = {"resultado": False}

    return JsonResponse(lista)


# Permite eliminar los datos validados
def eliminar_validados(request):
    estacion_id = int(request.POST.get("estacion_id", None))
    variable_id = int(request.POST.get("variable_id", None))
    cambios_json = request.POST.get("cambios", None)

    variable = Variable.objects.get(var_id=variable_id)

    cambios_lista = json.loads(cambios_json)
    condiciones = functions.get_condiciones(cambios_lista)
    resultado = functions.eliminar_datos_validacion(
        cambios_lista, variable, estacion_id, condiciones
    )
    lista = {"resultado": resultado}

    return JsonResponse(lista)


# Permite eliminar los datos validados
def eliminar_validados(request):
    estacion_id = int(request.POST.get("estacion_id", None))
    variable_id = int(request.POST.get("variable_id", None))
    cambios_json = request.POST.get("cambios", None)

    variable = Variable.objects.get(var_id=variable_id)

    cambios_lista = json.loads(cambios_json)
    condiciones = functions.get_condiciones(cambios_lista)
    resultado = functions.eliminar_datos_validacion(
        cambios_lista, variable, estacion_id, condiciones
    )
    lista = {"resultado": resultado}

    return JsonResponse(lista)


class ValidacionList(LoginRequiredMixin, FormView):
    template_name = "validacion_v2/periodos_validacion.html"
    form_class = ValidationSearchForm
    success_url = "/medicion/filter/"
    lista = []

    def post(self, request, *args, **kwargs):
        estacion_id = None
        variable_id = None
        try:
            estacion_id = int(request.POST.get("estacion", None))
            variable_id = int(request.POST.get("variable", None))
            m = "Var" + str(variable_id) + "Medicion"
            m = globals()[m]
            fechaa = m.objects.filter(estacion_id__exact=estacion_id).aggregate(
                Max("fecha"), Min("fecha")
            )
            # print(fechaa['fecha__min'])
            inicio = str(fechaa["fecha__min"])
            # print(inicio)
            variable = Variable.objects.get(var_id=variable_id)
            # res = variable.var_modelo.lower()
        except:
            pass

        intervalos = functions.periodos_validacion2(estacion_id, variable, inicio)
        return render(request, self.template_name, {"intervalos": intervalos})
