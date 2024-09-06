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

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from formatting.models import Format
from management.models import PermissionsBase
from station.models import Station

User = get_user_model()


class DataImport(PermissionsBase):
    STATUS = (("N", "Not queued"), ("Q", "Queued"), ("C", "Completed"), ("F", "Failed"))

    data_import_id = models.AutoField("Id", primary_key=True)
    station = models.ForeignKey(Station, models.PROTECT, verbose_name="Station")
    format = models.ForeignKey(Format, models.PROTECT, verbose_name="Format")
    rawfile = models.FileField("Data file", blank=False, null=False)
    date = models.DateTimeField("Submission date", auto_now_add=True)
    start_date = models.DateTimeField("Start date", blank=True, null=True)
    end_date = models.DateTimeField("End date", blank=True, null=True)
    records = models.IntegerField("Records", blank=True, null=True)
    observations = models.TextField("Observations/Notes", blank=True, null=True)
    status = models.TextField(
        "Status", choices=STATUS, help_text="Status of the import", default="N"
    )
    log = models.TextField(
        "Data ingestion log",
        help_text="Log of the data ingestion, indicating any errors",
        default="",
    )
    reprocess = models.BooleanField(
        "Reprocess data",
        help_text="If checked, the data will be reprocessed",
        default=False,
    )

    def get_absolute_url(self):
        return reverse("importing:data_import_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.station}/{self.owner}/{self.date}"

    def clean(self) -> None:
        """Validate information and uploads the measurement data."""
        tz = self.station.timezone
        if not tz:
            raise ValidationError("Station must have a timezone set.")

        if self.reprocess:
            self.status = "N"
            self.reprocess = False
