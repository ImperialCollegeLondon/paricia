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

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

from formatting.models import Format
from station.models import Station

User = get_user_model()


class DataImportBase(models.Model):
    """
    Base class used for full and temporary import of data files.
    start_date and end_date refer to the first and last dates of the data and are
    populated automatically from the data file. They are used to check whether any
    existing data from this station would be overwritten upon import.
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
    user = models.ForeignKey(
        User, models.SET_NULL, blank=True, null=True, verbose_name="User"
    )

    def __str__(self):
        return f"{self.station}/{self.user}/{self.date}"

    class Meta:
        abstract = True


class DataImportTemp(DataImportBase):
    """
    Used for importing data temporarily before full import to the database.
    """

    file = models.FileField("File", upload_to="files/tmp/")

    def get_absolute_url(self):
        return reverse("importing:data_import_temp_detail", kwargs={"pk": self.pk})

    class Meta:
        default_permissions = ()


class DataImportFull(DataImportBase):
    """
    Used for importing data permanently (fully) to the database.
    """

    file = models.FileField("File", upload_to="files/", blank=True, null=True)
    import_temp = models.ForeignKey(
        DataImportTemp, on_delete=models.CASCADE, null=True, blank=True
    )

    def get_absolute_url(self):
        return reverse("importing:data_import_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("-date",)
        permissions = [
            (
                "download_original_file",
                "Download the original file that was uploaded to the system.",
            ),
        ]
