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
from variable.models import SensorInstallation, Variable

User = get_user_model()


class DataImport(PermissionsBase):
    """Model to store the data imports.

    This model stores the data imports, which are files with data that are uploaded to
    the system. The data is then processed asynchronously and stored in the database.

    Attributes:
        station (ForeignKey): Station to which the data belongs.
        format (ForeignKey): Format of the data.
        rawfile (FileField): File with the data to be imported.
        date (DateTimeField): Date of submission of the data.
        start_date (DateTimeField): Start date of the data.
        end_date (DateTimeField): End date of the data.
        records (IntegerField): Number of records in the data.
        observations (TextField): Notes or observations about the data.
        status (TextField): Status of the import.
        log (TextField): Log of the data ingestion, indicating any errors.
        reprocess (BooleanField): If checked, the data will be reprocessed.
    """

    STATUS = (("N", "Not queued"), ("Q", "Queued"), ("C", "Completed"), ("F", "Failed"))

    data_import_id = models.AutoField("Id", primary_key=True, help_text="Primary key.")
    station = models.ForeignKey(
        Station,
        models.PROTECT,
        verbose_name="Station",
        help_text="Station to which the data belongs.",
    )
    format = models.ForeignKey(
        Format, models.PROTECT, verbose_name="Format", help_text="Format of the data."
    )
    rawfile = models.FileField(
        "Data file",
        blank=False,
        null=False,
        help_text="File with the data to be imported.",
    )
    date = models.DateTimeField(
        "Submission date",
        auto_now_add=True,
        help_text="Date of submission of the data.",
    )
    start_date = models.DateTimeField(
        "Start date", blank=True, null=True, help_text="Start date of the data."
    )
    end_date = models.DateTimeField(
        "End date", blank=True, null=True, help_text="End date of the data."
    )
    records = models.IntegerField(
        "Records", blank=True, null=True, help_text="Number of records in the data."
    )
    observations = models.TextField(
        "Observations/Notes",
        blank=True,
        null=True,
        help_text="Notes or observations about the data.",
    )
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
        return reverse("importing:dataimport_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.station}/{self.owner}/{self.date}"

    def clean(self) -> None:
        """Validate information and uploads the measurement data."""
        tz = self.station.timezone
        if not tz:
            raise ValidationError("Station must have a timezone set.")

        # If the file has changed, we reprocess the data
        if self.pk and self.rawfile != self.__class__.objects.get(pk=self.pk).rawfile:
            self.reprocess = True

        if self.reprocess:
            self.status = "N"
            self.reprocess = False


class ThingsboardImportMap(models.Model):
    """Model to store Thingsboard device mappings to station variables.

    This model maps Thingsboard devices to specific variables at stations, allowing
    data from IoT devices to be imported and associated with the correct station and
    variable combinations.

    Attributes:
        name (CharField): Name of the mapping.
        variable (ForeignKey): Variable associated with this mapping.
        device_id (CharField): Thingsboard device identifier.
        station (ForeignKey): Station to which the device data belongs.
    """

    name = models.CharField(
        "Name",
        max_length=255,
        blank=False,
        null=False,
        help_text="Name of the mapping.",
    )
    variable = models.ForeignKey(
        Variable,
        models.PROTECT,
        verbose_name="Variable",
        blank=False,
        null=False,
        help_text="Variable name in the data import.",
    )

    device_id = models.CharField(
        "Device ID",
        max_length=255,
        blank=False,
        null=False,
        help_text="Id of the thingsboard device.",
    )
    station = models.ForeignKey(
        Station,
        models.PROTECT,
        verbose_name="Station",
        help_text="Station to which the data belongs.",
    )

    def __str__(self):
        return f"{self.name} - {self.variable} - {self.device_id}"

    def clean(self) -> None:
        """Validate that the variable is valid for the station."""
        super().clean()
        if self.variable and self.station:
            # Check if the variable is valid for the station through SensorInstallation
            if not SensorInstallation.objects.filter(
                variable=self.variable, station=self.station
            ).exists():
                raise ValidationError(
                    {
                        "variable": f'Variable "{self.variable}" is not configured for station "{self.station}".'  # noqa E501
                    }
                )
