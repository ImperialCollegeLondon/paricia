########################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos
# (iMHEA)basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#           Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS),
#           Ecuador.
#           Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones
#  creadoras, ya sea en uso total o parcial del código.
########################################################################################

from __future__ import unicode_literals

import copy
import json
import mimetypes
import urllib

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Value
from django.db.models.functions import Concat
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from home.functions import *
from importacion.forms import ImportacionForm
from importacion.functions import *
from importacion.models import Importacion, ImportacionTemp


class ImportacionList(PermissionRequiredMixin, TemplateView):
    template_name = "importacion/importacion_list.html"
    permission_required = "importacion.view_importacion"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = [
            "imp_id",
            "station_id__station_code",
            "for_id__for_nombre",
            "imp_fecha",
            "imp_fecha_ini",
            "imp_fecha_fin",
            "imp_archivo",
            "imp_observacion",
            "usuario__username",
        ]
        importacion = Importacion.objects.all().values_list(*campos)
        context["importacion"] = modelo_a_tabla_html(importacion, col_extra=True)
        return context


class ImportacionDetail(PermissionRequiredMixin, DetailView):
    permission_required = "importacion.view_importacion"
    model = Importacion
    template_name = "importacion/importacion_detail.html"
    existe_vacio = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        informacion, self.existe_vacio = validar_fechas(self.object)
        context["informacion"] = informacion
        return context


@permission_required("importacion.descarga_archivo_original")
def ImportacionDescarga(request, *args, **kwargs):
    if request.user.is_authenticated:
        imp_id = kwargs.get("pk")
        importacion = Importacion.objects.get(imp_id=imp_id)
        file_path = "media/" + str(importacion.imp_archivo)
        output_filename = os.path.basename(file_path)
        fp = open(file_path, "rb")
        response = HttpResponse(fp.read())
        fp.close()
        type, encoding = mimetypes.guess_type(output_filename)
        if type is None:
            type = "application/octet-stream"
        response["Content-Type"] = type
        response["Content-Length"] = str(os.stat(file_path).st_size)
        if encoding is not None:
            response["Content-Encoding"] = encoding

        # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
        if "WebKit" in request.META["HTTP_USER_AGENT"]:
            # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
            # filename_header = 'filename=%s' % output_filename.encode('utf-8')
            filename_header = "filename=%s" % urllib.parse.quote(
                output_filename.encode("utf-8")
            )
        elif "MSIE" in request.META["HTTP_USER_AGENT"]:
            # IE does not support internationalized filename at all.
            # It can only recognize internationalized URL, so we do the trick via routing rules.
            filename_header = ""
        else:
            # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
            # filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(output_filename.encode('utf-8'))
            filename_header = "filename*=UTF-8''%s" % urllib.parse.quote(
                output_filename.encode("utf-8")
            )
        response["Content-Disposition"] = "attachment; " + filename_header
        return response


class ImportacionTempCreate(PermissionRequiredMixin, CreateView):
    permission_required = "importacion.add_importacion"
    model = ImportacionTemp
    fields = ["station_id", "for_id", "imp_archivo"]
    template_name = "importacion/importacion_form.html"

    def form_valid(self, form):
        archivo = copy.deepcopy(self.request.FILES["imp_archivo"])
        matriz = preformato_matriz(archivo, form.cleaned_data["for_id"])
        del archivo
        form.instance.imp_fecha_ini = matriz.loc[0, "fecha"]
        form.instance.imp_fecha_fin = matriz.loc[matriz.shape[0] - 1, "fecha"]
        form.instance.usuario = self.request.user
        return super(ImportacionTempCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ImportacionTempCreate, self).get_context_data(**kwargs)
        context["title"] = "Subir Archivo"
        return context


class ImportacionTempDetail(PermissionRequiredMixin, DetailView, FormView):
    permission_required = "importacion.add_importacion"
    model = ImportacionTemp
    template_name = "importacion/importaciontemp_detail.html"
    form_class = ImportacionForm
    sobrescribe = False

    def post(self, request, *args, **kwargs):
        form = ImportacionForm(request.POST or None)
        if form.is_valid():
            if request.POST["accion"] == "confirmar":
                imp_id__temp = kwargs.get("pk")
                imp_id = guardar_datos__temp_a_final(imp_id__temp, form)
                importacion = Importacion.objects.get(imp_id=imp_id)
                clasificaciones = importacion.for_id.clasificacion_set.all()
                variables = []
                for clasificacion in clasificaciones:
                    variables.append(clasificacion.var_id_id)
                if 11 in variables:
                    insertar_nivel_regleta(
                        importacion, json.loads(request.POST["nivelregleta"])
                    )
                return render(
                    request,
                    "importacion/mensaje.html",
                    {"mensaje": "Informacion Cargada"},
                )
            elif request.POST["accion"] == "cancelar":
                return self.render_to_response(self.get_context_data(form=form))
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(ImportacionTempDetail, self).get_context_data(**kwargs)
        informacion, self.sobrescribe = validar_fechas(self.object)
        context["informacion"] = informacion
        context["sobrescribe"] = self.sobrescribe
        context["nombre_archivo_solo"] = os.path.basename(self.object.imp_archivo.name)
        return context


# lista de formatos por station y datalogger
@permission_required("importacion.add_importacion")
def lista_formatos(request):
    station_id = request.GET.get("station", None)
    datos = consultar_formatos(station_id)
    return JsonResponse(datos)
