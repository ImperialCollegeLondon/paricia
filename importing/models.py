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

import tempfile
from enum import StrEnum, auto
from pathlib import Path

import pandas as pd
import rioxarray  # noqa: F401
import xarray as xr
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse

from djangomain import settings
from formatting.models import Format
from importing.utils import validate_layer_file_size
from management.models import PermissionsBase
from station.models import Station
from variable.models import SensorInstallation, Variable

User = get_user_model()

MAX_FILE_SIZE = settings.MAX_LAYER_FILE_SIZE_MB


class FileType(StrEnum):
    """File types supported by the MapLayerImport model."""

    GEOTIFF = auto()
    NETCDF = auto()


class ImportOrigin(models.Model):
    """Class that contains the origin of the data import, eg. file, API, etc."""

    origin = models.CharField(
        "Origin",
        blank=False,
        null=False,
        help_text="Origin of the data imported.",
    )

    def __str__(self):
        return self.origin

    @classmethod
    def get_default(cls) -> ImportOrigin:
        """Get default import origin, 'file'.

        It should exist, as it is created in a data migration, but just in case it
        is not, we use get_or_create.
        """
        obj, _ = cls.objects.get_or_create(origin="file")
        return obj.pk


class DataImport(PermissionsBase):
    """Model to store the data imports.

    This model stores the data imports, which are, often, files with data that are
    uploaded to the system. The data is then processed asynchronously and stored in the
    database.

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
        Format,
        models.PROTECT,
        verbose_name="Format",
        help_text="Format of the data.",
    )
    origin = models.ForeignKey(
        ImportOrigin,
        models.PROTECT,
        default=ImportOrigin.get_default,
        help_text="Origin of the imported data",
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

    def get_absolute_url(self):
        return reverse("importing:dataimport_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.station}/{self.owner}/{self.date}"

    def clean(self) -> None:
        """Validate information and uploads the measurement data."""
        tz = self.station.timezone
        if not tz:
            raise ValidationError("Station must have a timezone set.")

        if self.origin.origin == "Thingsboard" and not self.format.thingsboard:
            raise ValidationError("Ensure a Thingsboard-specific format is specified.")


class ThingsboardImportMap(PermissionsBase):
    """Model to store Thingsboard device mappings to station variables.

    This model maps Thingsboard devices to specific variables at stations, allowing
    data from IoT devices to be imported and associated with the correct station and
    variable combinations.

    Attributes:
        tb_variable (CharField): Name of the variable in Thingsboard.
        variable (ForeignKey): The existing variable in Paricia associated with this mapping.
        tb_device_name (CharField): The name of the device in Thingsboard.
        station (ForeignKey): The name of the corresponding station in Paricia.
    """  # noqa E501

    tb_variable = models.CharField(
        "Thingsboard Variable",
        max_length=255,
        blank=False,
        null=False,
        help_text="The name of the variable in Thingsboard.",
    )
    variable = models.ForeignKey(
        Variable,
        models.PROTECT,
        verbose_name="Variable",
        blank=False,
        null=False,
        help_text="Variable name in the data import.",
    )
    station = models.ForeignKey(
        Station,
        models.PROTECT,
        verbose_name="Station",
        help_text="The name of the corresponding station in Paricia.",
    )
    tb_device_name = models.CharField(
        "Thingsboard Device Name",
        max_length=255,
        help_text="The name of the device in Thingsboard.",
    )

    def __str__(self):
        return f"{self.tb_device_name} -> {self.station}: {self.tb_variable} -> {self.variable}"  # noqa E501

    def clean(self) -> None:
        """Validate that the variable is valid for the station."""
        try:
            station = self.station
        except ThingsboardImportMap.station.RelatedObjectDoesNotExist:
            raise ValidationError({"station": "Station is required."})

        try:
            variable = self.variable
        except ThingsboardImportMap.variable.RelatedObjectDoesNotExist:
            raise ValidationError({"variable": "Variable is required."})

        # Check if the variable is valid for the station through SensorInstallation
        if not SensorInstallation.objects.filter(
            variable=variable, station=station
        ).exists():
            raise ValidationError(
                {
                    "variable": f"Variable '{variable}' is not configured for"
                    f" station '{station}' via a sensor installation."
                }
            )

    def get_absolute_url(self):
        return reverse("importing:thingsboardimportmap_detail", kwargs={"pk": self.pk})


class MapLayerImport(PermissionsBase):
    name = models.CharField(
        "Name",
        max_length=255,
        blank=False,
        null=False,
        help_text="Name of the layer to be imported.",
    )
    description = models.TextField(
        "Description",
        blank=True,
        null=True,
        help_text="Description of the layer to be imported.",
    )
    file = models.FileField(
        "Layer file",
        blank=False,
        help_text=f"Must be a tiff file. File size must not exceed {MAX_FILE_SIZE} MB",
        validators=[
            FileExtensionValidator(allowed_extensions=["tif", "tiff", "nc"]),
            validate_layer_file_size,
        ],
    )
    updated_at = models.DateTimeField(
        "Updated at",
        auto_now=True,
        help_text="The time at which the layer was last updated.",
    )
    variable = models.CharField(
        "Variable",
        max_length=50,
        blank=True,
        null=True,
        help_text="Variable associated with the map layer, required to extract data "
        "from NetCDF files.",
    )
    timestamps = models.JSONField(
        "Timestamps",
        blank=True,
        null=True,
        help_text="List of dates associated with the map layer if from a NetCDF file.",
    )

    @property
    def file_type(self) -> FileType:
        """Infer the file type from the extension."""
        ext = Path(self.file.name).suffix.lower()
        if ext in [".tif", ".tiff"]:
            return FileType.GEOTIFF
        return FileType.NETCDF

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("importing:maplayerimport_detail", kwargs={"pk": self.pk})

    @staticmethod
    def _read_geotiff_metadata(
        file_obj: File,
    ) -> tuple[str, tuple[float, float, float, float]]:
        """Read the coordinate reference system (crs) and bounds from a GeoTIFF file.

        Args:
            file_obj: The GeoTIFF file object to read metadata from.

        Returns:
            The CRS and bounds of the GeoTIFF file.
        """
        import rasterio

        with rasterio.MemoryFile(file_obj.read()) as memfile:
            with memfile.open() as dataset:
                if dataset.count == 0:
                    raise ValidationError({"file": "File contains no raster bands."})

        return dataset.crs, dataset.bounds

    def _read_netcdf_metadata(
        self, file_obj: File
    ) -> tuple[str, tuple[float, float, float, float]]:
        """Read the coordinate reference system (crs) and bounds from a NetCDF file.

        Args:
            file_obj: The NetCDF file object to read metadata from.

        Returns:
            The CRS and bounds of the NetCDF file.
        """
        with tempfile.NamedTemporaryFile(suffix=".nc") as tmp:
            tmp.write(file_obj.read())
            tmp.flush()

            with xr.open_dataset(tmp.name, engine="netcdf4", decode_coords="all") as ds:
                if self.variable not in ds:
                    raise ValidationError(
                        {
                            "variable": f"Variable '{self.variable}' not found in "
                            "NetCDF file."
                        }
                    )

                data = ds[self.variable]
                if data.size == 0:
                    raise ValidationError(
                        {
                            "variable": f"No data found for variable '{self.variable}' "
                            "in NetCDF file."
                        }
                    )

                if "t" not in data.dims:
                    raise ValidationError(
                        {
                            "variable": f"Variable '{self.variable}' must have a "
                            "temporal dimension named 't'."
                        }
                    )
                # Save timestamps as a list in the timestamps field
                try:
                    timestamps = [
                        pd.to_datetime(timestamp).strftime("%d-%m-%Y")
                        for timestamp in data["t"].values
                    ]
                    self.timestamps = timestamps
                except Exception as e:
                    raise ValidationError(
                        {
                            "variable": "Could not read timestamps for variable '"
                            f"{self.variable}': {e}"
                        }
                    )

                if "x" not in data.dims or "y" not in data.dims:
                    raise ValidationError(
                        {
                            "variable": f"Variable '{self.variable}' must have 'x' and "
                            "'y' spatial dimensions."
                        }
                    )
                data = data.rio.set_spatial_dims(x_dim="x", y_dim="y")
                return data.rio.crs, data.rio.bounds()

    def clean(self) -> None:
        """Validate the uploaded file and its transformed lon/lat bounds."""

        if not self.file:
            return

        if self.file_type == "netcdf" and not self.variable:
            raise ValidationError(
                {"variable": "Variable is required for NetCDF files."}
            )

        from rasterio.warp import transform_bounds

        file_obj = self.file.file

        try:
            if self.file_type == "geotiff":
                crs, bounds = self._read_geotiff_metadata(file_obj)
            else:
                crs, bounds = self._read_netcdf_metadata(file_obj)

            if crs is None:
                raise ValidationError(
                    {"file": "File has no coordinate reference system (CRS)."}
                )

            left, bottom, right, top = transform_bounds(crs, "EPSG:4326", *bounds)

            if not (-180 <= left <= 180 and -180 <= right <= 180):
                raise ValidationError(
                    {"file": ("Longitude values are out of range [-180, 180].")}
                )
            if not (-90 <= bottom <= 90 and -90 <= top <= 90):
                raise ValidationError(
                    {"file": ("Latitude values are out of range [-90, 90].")}
                )

        except ValidationError:
            raise

        except Exception as e:
            raise ValidationError(
                {"file": f"Could not open as a valid file or read coordinates: {e}"}
            )
        finally:
            file_obj.seek(0)
