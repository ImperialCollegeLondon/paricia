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
import os
import urllib

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from home.functions import modelo_a_tabla_html
from importing.forms import DataImportForm
from importing.functions import (
    insert_level_rule,
    preformat_matrix,
    query_formats,
    save_temp_data_to_permanent,
    validate_dates,
)
from importing.models import DataImportFull, DataImportTemp


class DataImportFullList(PermissionRequiredMixin, TemplateView):
    template_name = "importacion/importacion_list.html"
    permission_required = "importacion.view_dataimportfull"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = [
            "data_import_id",
            "station__station_code",
            "format__name",
            "date",
            "start_date",
            "end_date",
            "file",
            "observations",
            "user__username",
        ]
        data_import = DataImportFull.objects.all().values_list(*fields)
        context["data_import"] = modelo_a_tabla_html(data_import, col_extra=True)
        return context


class DataImportFullDetail(PermissionRequiredMixin, DetailView):
    permission_required = "importacion.view_dataimportfull"
    model = DataImportFull
    template_name = "importacion/importacion_detail.html"
    # existing_data = True if there exists data already for these dates.
    existing_data = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        information, self.existing_data = validate_dates(self.object)
        context["information"] = information
        return context


@permission_required("importacion.download_original_file")
def DataImportDownload(request, *args, **kwargs):
    """
    Download the original file from a data upload.
    """
    if request.user.is_authenticated:
        imp_id = kwargs.get("pk")
        data_import = DataImportFull.objects.get(data_import_id=imp_id)
        file_path = "media/" + str(data_import.file)
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
            # It can only recognize internationalized URL, so we do the trick via
            # routing rules.
            filename_header = ""
        else:
            # For others like Firefox, we follow RFC2231 (encoding extension in HTTP
            # headers).
            # filename_header = 'filename*=UTF-8\'\'%s' %
            # urllib.quote(output_filename.encode('utf-8'))
            filename_header = "filename*=UTF-8''%s" % urllib.parse.quote(
                output_filename.encode("utf-8")
            )
        response["Content-Disposition"] = "attachment; " + filename_header
        return response


class DataImportTempCreate(PermissionRequiredMixin, CreateView):
    permission_required = "importacion.add_dataimportfull"
    model = DataImportTemp
    fields = ["station", "format", "file"]
    template_name = "importacion/importacion_form.html"

    def form_valid(self, form):
        file = copy.deepcopy(self.request.FILES["file"])
        matrix = preformat_matrix(file, form.cleaned_data["format"])
        del file
        form.instance.start_date = matrix.loc[0, "date"]
        form.instance.end_date = matrix.loc[matrix.shape[0] - 1, "date"]
        form.instance.user = self.request.user
        return super(DataImportTempCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DataImportTempCreate, self).get_context_data(**kwargs)
        context["title"] = "Upload File"
        return context


class DataImportTempDetail(PermissionRequiredMixin, DetailView, FormView):
    permission_required = "importacion.add_dataimportfull"  # TODO: is this right?
    model = DataImportTemp
    template_name = "importacion/importaciontemp_detail.html"
    form_class = DataImportForm
    overwrite = False

    def post(self, request, *args, **kwargs):
        form = DataImportForm(request.POST or None)
        if form.is_valid():
            if request.POST["action"] == "confirm":
                imp_id__temp = kwargs.get("pk")
                imp_id = save_temp_data_to_permanent(imp_id__temp, form)
                data_import = DataImportFull.objects.get(imp_id=imp_id)
                classifications = data_import.format.classification_set.all()
                variables = []
                for classification in classifications:
                    variables.append(classification.variable_id)
                if 11 in variables:
                    insert_level_rule(
                        data_import, json.loads(request.POST["level_rule"])
                    )
                return render(
                    request,
                    "importacion/mensaje.html",
                    {"mensaje": "Informacion Cargada"},
                )
            elif request.POST["action"] == "cancel":
                return self.render_to_response(self.get_context_data(form=form))
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(DataImportTempDetail, self).get_context_data(**kwargs)
        information, self.overwrite = validate_dates(self.object)
        context["information"] = information
        context["overwrite"] = self.overwrite
        context["file_name_only"] = os.path.basename(self.object.file.name)
        return context


@permission_required("importacion.add_importacion")
def list_formats(request):
    """
    list of formats per station.
    """
    station_id = request.GET.get("station", None)
    data = query_formats(station_id)
    return JsonResponse(data)
