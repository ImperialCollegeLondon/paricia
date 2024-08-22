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
import shutil
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from formatting.models import Format
from management.models import PermissionsBase
from station.models import Station

from .functions import read_data_to_import, save_temp_data_to_permanent

User = get_user_model()


class DataImportTemp(PermissionsBase):
    """Used for importing data temporarily before full import to the database.
    start_date and end_date refer to the first and last dates of the data and are
    populated automatically from the data file. They are used to flag whether any
    existing data from this station would be overwritten upon import.
    TODO: Rename to DataImportInitial.
    """

    data_import_id = models.AutoField("Id", primary_key=True)
    station = models.ForeignKey(
        Station, models.SET_NULL, blank=True, null=True, verbose_name="Station"
    )
    format = models.ForeignKey(
        Format, models.SET_NULL, blank=True, null=True, verbose_name="Format"
    )
    date = models.DateTimeField("Date", auto_now_add=True)
    start_date = models.DateTimeField("Start date", default=timezone.now)
    end_date = models.DateTimeField("End date", default=timezone.now)
    observations = models.TextField("Observations/Notes", blank=True, null=True)

    file = models.FileField("File", upload_to="files/tmp/")

    def get_absolute_url(self):
        return reverse("importing:data_import_temp_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.station}/{self.owner}/{self.date}"

    def clean(self) -> None:
        """Check that the station has a timezone set and get start and end dates."""
        tz = self.station.timezone
        if tz is None:
            raise ValidationError("Station must have a timezone set.")

        data = read_data_to_import(self.file, self.format, tz)
        self.start_date = data["date"].iloc[0]
        self.end_date = data["date"].iloc[-1]
        del data
        return


class DataImportFull(PermissionsBase):
    """Used for importing data permanently (fully) to the database. Simply relates
    a DataImportTemp object to the new, permanent file location.
    """

    date = models.DateTimeField("Date", auto_now_add=True)
    filepath = models.CharField("File", max_length=1024, blank=True, null=True)
    import_temp = models.ForeignKey(
        DataImportTemp, on_delete=models.CASCADE, null=True, blank=True
    )

    def get_absolute_url(self):
        return reverse("importing:data_import_detail", kwargs={"pk": self.pk})

    def clean(self) -> None:
        """Read the data from the temp file and save it to the database.

        The temporary file is moved to the permanent location and the filepath field is
        set accordingly.
        """

        # Actually read the data and save it to the database
        save_temp_data_to_permanent(self.import_temp)

        # Move the file from tmp to permanent and set the filepath field accordingly
        tmp_file_path = Path(settings.MEDIA_ROOT) / Path(str(self.import_temp.file))
        final_file_path = Path(settings.MEDIA_ROOT) / "files"
        self.filepath = str(final_file_path)
        shutil.copy(tmp_file_path, final_file_path)
