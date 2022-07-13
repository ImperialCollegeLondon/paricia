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
import shutil
import urllib

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from rest_framework import generics

from djangomain.settings import BASE_DIR
from importing.forms import DataImportForm
from importing.functions import (
    insert_level_rule,
    preformat_matrix,
    query_formats,
    save_temp_data_to_permanent,
    validate_dates,
)
from importing.models import DataImportFull, DataImportTemp

from .serializers import DataImportFullSerializer, DataImportTempSerializer


class DataImportTempList(generics.ListAPIView):
    queryset = DataImportTemp.objects.all()
    serializer_class = DataImportTempSerializer


class DataImportTempCreate(generics.CreateAPIView):
    serializer_class = DataImportTempSerializer

    def perform_create(self, serializer):
        file = copy.deepcopy(self.request.FILES["file"])
        matrix = preformat_matrix(file, serializer.validated_data["format"])
        del file
        # Set start and end date based on cleaned data from the file
        serializer.validated_data["start_date"] = matrix.loc[0, "date"]
        serializer.validated_data["end_date"] = matrix.loc[matrix.shape[0] - 1, "date"]
        # Set user from the request
        serializer.validated_data["user"] = self.request.user
        serializer.save()


class DataImportTempDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DataImportTemp.objects.all()
    serializer_class = DataImportTempSerializer

    # TODO: will this still work with the DRF?
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        information, self.existing_data = validate_dates(self.object)
        context["information"] = information
        return context


class DataImportFullList(generics.ListAPIView):
    queryset = DataImportFull.objects.all()
    serializer_class = DataImportFullSerializer


class DataImportFullCreate(generics.CreateAPIView):
    serializer_class = DataImportFullSerializer

    def perform_create(self, serializer):
        serializer.validated_data["user"] = self.request.user

        # Save the actual measurement data
        save_temp_data_to_permanent(serializer.validated_data["import_temp"])

        # Move the file from tmp to permanent and set the filepath field accordingly
        tmp_file_path = "media/" + str(serializer.validated_data["import_temp"].file)
        final_file_path = str(
            serializer.validated_data["import_temp"].file.path
        ).replace("files/tmp/", "files/")
        serializer.validated_data["filepath"] = str(final_file_path)
        shutil.copy(tmp_file_path, final_file_path)

        # Save the new object and remove the tmp file
        serializer.save()
        os.remove(tmp_file_path)


class DataImportFullDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DataImportFull.objects.all()
    serializer_class = DataImportFullSerializer

    # TODO: will this still work with the DRF?
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        information, self.existing_data = validate_dates(self.object)
        context["information"] = information
        return context


########################################################################


@permission_required("importing.download_original_file")
def DataImportDownload(request, *args, **kwargs):
    """
    Download the original file from a data upload.
    """
    if request.user.is_authenticated:
        imp_id = kwargs.get("pk")
        data_import = DataImportFull.objects.get(data_import_id=imp_id)
        file_path = str(data_import.filepath)
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


def list_formats(request):
    """
    list of formats per station.
    """
    station_id = request.GET.get("station", None)
    data = query_formats(station_id)
    return JsonResponse(data)
