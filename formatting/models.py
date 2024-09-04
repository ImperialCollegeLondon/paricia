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


from django.db import models
from django.urls import reverse

from management.models import PermissionsBase
from station.models import Station
from variable.models import Variable


class Extension(PermissionsBase):
    """Extension of the data file.

    It is mostly used to chose the tool to be employed to ingest the data. While it can
    take any value, there is currently explicit support only for `xlsx` and `xlx`.
    Anything else will be interpreted as a text file and loaded using `pandas.read_csv`.

    Attributes:
        extension_id (AutoField): Primary key.
        value (CharField): The extension value. eg. `xlsx`, `xlx`, `txt`.
    """

    extension_id = models.AutoField("Id", primary_key=True, help_text="Primary key.")
    value = models.CharField(
        "Value",
        max_length=5,
        help_text="The extension value. eg. `xlsx`, `xlx`, `txt`.",
    )

    def __str__(self):
        return str(self.value)

    def get_absolute_url(self):
        return reverse("format:extension_index")


class Delimiter(PermissionsBase):
    """Delimiter between columns in the data file.

    One or more characters that separate columns in a text file. The most common values
    are `,`, `;`, and `\\t` (tab).

    Attributes:
        delimiter_id (AutoField): Primary key.
        name (CharField): The name of the delimiter. eg. `comma`, `semicolon`, `tab`.
        character (CharField): The character used as a delimiter. eg. `,`, `;`, `\\t`.
    """

    delimiter_id = models.AutoField("Id", primary_key=True, help_text="Primary key.")
    name = models.CharField(
        "Name",
        max_length=100,
        help_text="The name of the delimiter. eg. `comma`, `semicolon`, `tab`.",
    )
    character = models.CharField(
        "Character",
        max_length=10,
        blank=True,
        help_text="The character used as a delimiter. eg. `,`, `;`, `\\t`.",
    )

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("format:delimiter_index")


class Date(PermissionsBase):
    """Date format.

    Format string for the date column. It is used to parse the date column in the data
    file. The format string must be compatible with the `datetime` module in Python. See
    the [datetime documentation](https://docs.python.org/3.11/library/datetime.html#format-codes)
    for more information on valid format codes.

    Attributes:
        date_id (AutoField): Primary key.
        date_format (CharField): The format string for the date column in human readable
            form, eg. `DD-MM-YYYY`.
        code (CharField): The code used to parse the date column, eg. `%d-%m-%Y`.
    """

    date_id = models.AutoField("Id", primary_key=True, help_text="Primary key.")
    date_format = models.CharField(
        "Format",
        max_length=20,
        help_text="The format string for the date column in human readable form, eg."
        "`DD-MM-YYYY`.",
    )
    code = models.CharField(
        "Code",
        max_length=20,
        help_text="The code used to parse the date column, eg. `%d-%m-%Y`.",
    )

    def __str__(self):
        return str(self.date_format)

    def get_absolute_url(self):
        return reverse("format:date_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("date_id",)


class Time(PermissionsBase):
    """Time format.

    Format string for the time column. It is used to parse the time column in the data
    file. The format string must be compatible with the `datetime` module in Python. See
    the [datetime documentation](https://docs.python.org/3.11/library/datetime.html#format-codes)
    for more information on valid format codes.

    Attributes:
        date_id (AutoField): Primary key.
        date_format (CharField): The format string for the date column in human readable
            form, eg. `HH:MM:SS 24H`.
        code (CharField): The code used to parse the date column, eg. `%H:%M:%S`.
    """

    time_id = models.AutoField("Id", primary_key=True, help_text="Primary key.")
    time_format = models.CharField(
        "Format",
        max_length=20,
        help_text="The format string for the date column in human readable form, eg. "
        "`HH:MM:SS 24H`",
    )
    code = models.CharField("Code", max_length=20)

    def __str__(self):
        return str(self.time_format)

    def get_absolute_url(self):
        return reverse("format:time_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("time_id",)


class Format(PermissionsBase):
    """Details of the data file format, describing how to read the file.

    It combines several properties, such as the file extension, the delimiter, the date
    and time formats, and the column indices for the date and time columns, instructing
    how to read the data file and parse the dates. It is mostly used to ingest data from
    text files, like CSV.

    Attributes:
        format_id (AutoField): Primary key.
        name (CharField): Short name of the format entry.
        description (TextField): Description of the format.
        extension (ForeignKey): The extension of the data file.
        delimiter (ForeignKey): The delimiter between columns in the data file. Only
            required for text files.
        first_row (SmallIntegerField): First row of the data, excluding any heading.
        footer_rows (SmallIntegerField): Number of footer rows, to be ignored at the
            end.
        date (ForeignKey): Format for the date column. Only required for text files.
        date_column (SmallIntegerField): Index of the date column, starting in 1.
        time (ForeignKey): Format for the time column. Only required for text files.
        time_column (SmallIntegerField): Index of the time column, starting in 1.
    """

    format_id = models.AutoField(
        "format_id", primary_key=True, help_text="Primary key."
    )
    name = models.CharField(
        "Format name", max_length=35, help_text="Short name of the format entry."
    )
    description = models.TextField(
        "Description", blank=True, null=True, help_text="Description of the format."
    )
    extension = models.ForeignKey(
        Extension,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        verbose_name="File extension",
        help_text="The extension of the data file.",
    )
    delimiter = models.ForeignKey(
        Delimiter,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Delimiter",
        help_text="The delimiter between columns in the data file. Only required for "
        "text files.",
    )
    first_row = models.SmallIntegerField(
        "First row", help_text="First row of the data, excluding any heading."
    )
    footer_rows = models.SmallIntegerField(
        "Number of footer rows",
        blank=True,
        null=False,
        default=0,
        help_text="Number of footer rows, to be ignored at the end.",
    )
    date = models.ForeignKey(
        Date,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Date format",
        help_text="Format for the date column. Only required for text files.",
    )
    date_column = models.SmallIntegerField(
        "Date column", help_text="Index of the date column, starting in 1."
    )
    time = models.ForeignKey(
        Time,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Time format",
        help_text="Format for the time column. Only required for text files.",
    )
    time_column = models.SmallIntegerField(
        "Time column", help_text="Index of the time column, starting in 1."
    )

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("format:format_detail", kwargs={"pk": self.pk})

    @property
    def datetime_format(self) -> str:
        return str(self.date.code) + " " + str(self.time.code)

    def datetime_columns(self, delimiter: str) -> list[int]:
        """Column indices that correspond to the date and time columns in the dataset.

        Args:
            delimiter (str): The delimiter used to split the date and time codes.

        Returns:
            list[int]: A list of column indices.
        """
        date_items = self.date.code.split(delimiter)
        date_cols = list(
            range(
                self.date_column - 1,
                self.date_column - 1 + len(date_items),
            )
        )
        time_items = self.time.code.split(delimiter)
        time_cols = list(
            range(
                self.time_column - 1,
                self.time_column - 1 + len(time_items),
            )
        )
        return date_cols + time_cols

    class Meta:
        ordering = ("-format_id",)


class Classification(PermissionsBase):
    """Classification details, combining several properties."""

    cls_id = models.AutoField("Id", primary_key=True)
    format = models.ForeignKey(Format, on_delete=models.PROTECT, verbose_name="Format")
    variable = models.ForeignKey(
        Variable, on_delete=models.PROTECT, verbose_name="Variable"
    )
    value = models.SmallIntegerField("Value column")
    maximum = models.SmallIntegerField("Maximum value column", blank=True, null=True)
    minimum = models.SmallIntegerField("Minimum value column", blank=True, null=True)
    value_validator_column = models.SmallIntegerField(
        "Value validator column", blank=True, null=True
    )
    value_validator_text = models.CharField(
        "Value validator text", max_length=10, blank=True, null=True
    )
    maximum_validator_column = models.SmallIntegerField(
        "Maximum value validator column", blank=True, null=True
    )
    maximum_validator_text = models.CharField(
        "Maximum value  validator text", max_length=10, blank=True, null=True
    )
    minimum_validator_column = models.SmallIntegerField(
        "Minimum value validator column", blank=True, null=True
    )
    minimum_validator_text = models.CharField(
        "Minimum value validator text", max_length=10, blank=True, null=True
    )
    accumulate = models.BooleanField("Accumulate every 5 min?", default=False)
    incremental = models.BooleanField("Is it an incremental counter?", default=False)
    resolution = models.DecimalField(
        "Resolution", max_digits=6, decimal_places=2, blank=True, null=True
    )
    decimal_comma = models.BooleanField(
        "Uses comma as decimal separator?", default=False
    )

    def __str__(self):
        return str(self.cls_id)

    def get_absolute_url(self):
        return reverse("format:classification_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("variable",)


class Association(PermissionsBase):
    """Associates a data format with a station."""

    association_id = models.AutoField("Id", primary_key=True)
    format = models.ForeignKey(
        Format, models.PROTECT, blank=True, null=True, verbose_name="Format"
    )
    station = models.ForeignKey(
        Station, models.PROTECT, blank=True, null=True, verbose_name="Station"
    )

    def get_absolute_url(self):
        return reverse("format:association_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("association_id",)
        unique_together = (
            "station",
            "format",
        )
