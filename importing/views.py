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


class DataImportTempDetailOld(PermissionRequiredMixin, DetailView, FormView):
    """
    This view acts as the detail view of the DataImportTemp objects and creates
    a new DataImportFull object. It also directly enters the measurement data into
    the database using the save_temp_data_to_permanent function.
    """

    permission_required = "importing.add_dataimportfull"  # TODO: is this right?
    model = DataImportTemp
    template_name = "importing/importingtemp_detail.html"
    form_class = DataImportForm
    overwrite = False

    def post(self, request, *args, **kwargs):
        form = DataImportForm(request.POST or None)
        if form.is_valid():
            if request.POST["action"] == "confirm":
                # Get the pk of the DataImportTemp object
                imp_id__temp = kwargs.get("pk")
                # Save the actual measurement data
                imp_id = save_temp_data_to_permanent(imp_id__temp, form)
                # Get the DataImportFull object as returned by the above function
                data_import = DataImportFull.objects.get(imp_id=imp_id)
                # Get the variables that are saved in this dataset
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
                    "importing/mensaje.html",
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


@permission_required("importing.add_importing")
def list_formats(request):
    """
    list of formats per station.
    """
    station_id = request.GET.get("station", None)
    data = query_formats(station_id)
    return JsonResponse(data)
