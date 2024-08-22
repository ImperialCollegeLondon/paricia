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

import copy
import os
import shutil

from django.core.exceptions import PermissionDenied
from rest_framework import generics

from djangomain.settings import BASE_DIR
from importing.functions import read_data_to_import, save_temp_data_to_permanent
from importing.models import DataImportFull, DataImportTemp

from .serializers import DataImportFullSerializer, DataImportTempSerializer


class DataImportTempList(generics.ListAPIView):
    """List all DataImportTemp objects. These are created when uploading a
    new data file. The measurement data is not saved until a DataImportFull object
    is created using an existing DataImportTemp object as a ForeignKey.
    """

    serializer_class = DataImportTempSerializer

    def get_queryset(self):
        return DataImportTemp.objects.filter(owner=self.request.user)


class DataImportTempCreate(generics.CreateAPIView):
    """Create a new DataImportTemp object. These are created when uploading a
    new data file. The measurement data is not saved until a DataImportFull object
    is created using an existing DataImportTemp object as a ForeignKey.
    """

    serializer_class = DataImportTempSerializer

    def perform_create(self, serializer):
        # Check permissions
        station = serializer.validated_data["station"]
        if not self.request.user.has_perm("station.change_station", station):
            raise PermissionDenied(
                "Only the station owner can add measurements for this station."
            )

        file = copy.deepcopy(self.request.FILES["file"])
        timezone = serializer.validated_data["station"].timezone
        if not timezone:
            raise ValueError(
                f"No timezone found! Setting timezone {timezone} for station "
                f"{serializer.validated_data['station']}."
            )
        data = read_data_to_import(file, serializer.validated_data["format"], timezone)
        del file
        # Set start and end date based on cleaned data from the file
        serializer.validated_data["start_date"] = data["date"].iloc[0]
        serializer.validated_data["end_date"] = data["date"].iloc[-1]
        # Set user from the request
        serializer.validated_data["owner"] = self.request.owner
        serializer.save()


class DataImportTempDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a DataImportTemp object.

    These are created when uploading a new data file. The measurement data is not saved
    until a DataImportFull object is created using an existing DataImportTemp object as
    a ForeignKey.
    """

    serializer_class = DataImportTempSerializer

    def get_queryset(self):
        return DataImportTemp.objects.filter(owner=self.request.user)


class DataImportFullList(generics.ListAPIView):
    """List all DataImportFull objects. These are created to save measurement data.
    A DataImportTemp object is required as a ForeignKey.
    """

    serializer_class = DataImportFullSerializer

    def get_queryset(self):
        return DataImportFull.objects.filter(owner=self.request.user)


class DataImportFullCreate(generics.CreateAPIView):
    """Create a new DataImportFull object. When these are created, the measurement data
    from a DataImportTemp object is imported into the database (into the measurement
    app).
    """

    queryset = DataImportFull.objects.all()
    serializer_class = DataImportFullSerializer

    def perform_create(self, serializer):
        serializer.validated_data["user"] = self.request.user

        # Check permissions
        station = serializer.validated_data["import_temp"].station
        if not self.request.user.has_perm("station.change_station", station):
            raise PermissionDenied(
                "Only the station owner can add measurements for this station."
            )

        # Save the actual measurement data
        save_temp_data_to_permanent(serializer.validated_data["import_temp"])

        # Move the file from tmp to permanent and set the filepath field accordingly
        tmp_file_path = (
            BASE_DIR
            + "/data/media/"
            + str(serializer.validated_data["import_temp"].file)
        )
        final_file_path = str(
            serializer.validated_data["import_temp"].file.path
        ).replace("files/tmp/", "files/")
        serializer.validated_data["filepath"] = str(final_file_path)
        shutil.copy(tmp_file_path, final_file_path)

        # Save the new object and remove the tmp file
        serializer.save()
        os.remove(tmp_file_path)

        # Create a new StripLevelReading object if appropriate.
        # TODO: This functionality is untested: insert_level_rule function needs
        # checking.
        classifications = serializer.validated_data[
            "import_temp"
        ].format.classification_set.all()
        variable_codes = [c.variable.variable_code for c in classifications]
        if "waterlevel" in variable_codes:
            pass
            # TODO work out how to implement below in DRF.
            # insert_level_rule(
            #    serializer.validated_data["import_temp"],
            #    json.loads(self.request.POST["level_rule"]),
            # )


class DataImportFullDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a DataImportFull object. These are created to save
    measurement data. A DataImportTemp object is required as a ForeignKey.
    """

    serializer_class = DataImportFullSerializer

    def get_queryset(self):
        return DataImportFull.objects.filter(owner=self.request.user)
