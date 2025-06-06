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

from collections import defaultdict

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from management.models import PermissionsBase
from variable.models import Variable


class Extension(PermissionsBase):
    """Extension of the data file.

    It is mostly used to choose the tool to be employed to ingest the data. While it can
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

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return str(self.value)

    def get_absolute_url(self) -> str:
        """Get the absolute URL of the object."""
        return reverse("formatting:extension_detail", kwargs={"pk": self.pk})


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

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return str(self.name)

    def get_absolute_url(self) -> str:
        """Get the absolute URL of the object."""
        return reverse("formatting:delimiter_detail", kwargs={"pk": self.pk})


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

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return str(self.date_format)

    def get_absolute_url(self) -> str:
        """Get the absolute URL of the object."""
        return reverse("formatting:date_detail", kwargs={"pk": self.pk})

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
    code = models.CharField(
        "Code",
        max_length=20,
        help_text="The code used to parse the date column, eg. `%H:%M:%S`",
    )

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return str(self.time_format)

    def get_absolute_url(self) -> str:
        """Get the absolute URL of the object."""
        return reverse("formatting:time_detail", kwargs={"pk": self.pk})

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
        first_row (PositiveSmallIntegerField): Index of the first row with data,
            starting in 0.
        footer_rows (PositiveSmallIntegerField): Number of footer rows to be ignored at
            the end.
        date (ForeignKey): Format for the date column. Only required for text files.
        date_column (PositiveSmallIntegerField): Index of the date column, starting in
            0.
        time (ForeignKey): Format for the time column. Only required for text files.
        time_column (PositiveSmallIntegerField): Index of the time column, starting in
            0.
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
    first_row = models.PositiveSmallIntegerField(
        "First row",
        default=1,
        help_text="Index of the first row with data, starting in 0.",
    )
    footer_rows = models.PositiveSmallIntegerField(
        "Number of footer rows",
        default=0,
        help_text="Number of footer rows to be ignored at the end.",
    )
    date = models.ForeignKey(
        Date,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Date format",
        help_text="Format for the date column. Only required for text files.",
    )
    date_column = models.PositiveSmallIntegerField(
        "Date column", default=0, help_text="Index of the date column, starting in 0."
    )
    time = models.ForeignKey(
        Time,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Time format",
        help_text="Format for the time column. Only required for text files.",
    )
    time_column = models.PositiveSmallIntegerField(
        "Time column", default=0, help_text="Index of the time column, starting in 0."
    )

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return str(self.name)

    def get_absolute_url(self) -> str:
        """Get the absolute URL of the object."""
        return reverse("formatting:format_detail", kwargs={"pk": self.pk})

    @property
    def datetime_format(self) -> str:
        """Obtain the datetime format string."""
        return str(self.date.code) + " " + str(self.time.code)

    def datetime_columns(self, delimiter: str) -> list[int]:
        """Column indices that correspond to the date and time columns in the dataset.

        Args:
            delimiter (str): The delimiter used to split the date and time codes.

        Returns:
            list[int]: A list of column indices.
        """
        date_items = self.date.code.split(delimiter)
        date_cols = list(range(self.date_column, self.date_column + len(date_items)))
        time_items = self.time.code.split(delimiter)
        time_cols = list(range(self.time_column, self.time_column + len(time_items)))
        return date_cols + time_cols

    class Meta:
        ordering = ("-format_id",)


class Classification(PermissionsBase):
    """Contains instructions on how to classify the data into a specific variable.

    In particular, it links a format to a variable, and provides the column indices for
    the value, maximum, and minimum columns, as well as the validator columns. It also
    contains information on whether the data is accumulated, incremental, and the
    resolution of the data.

    Attributes:
        cls_id (AutoField): Primary key.
        format (ForeignKey): The format of the data file.
        variable (ForeignKey): The variable to which the data belongs.
        value (PositiveSmallIntegerField): Index of the value column, starting in 0.
        maximum (PositiveSmallIntegerField): Index of the maximum value column, starting
            in 0.
        minimum (PositiveSmallIntegerField): Index of the minimum value column, starting
            in 0.
        value_validator_column (PositiveSmallIntegerField): Index of the value validator
            column, starting in 0.
        value_validator_text (CharField): Value validator text.
        maximum_validator_column (PositiveSmallIntegerField): Index of the maximum value
            validator column, starting in 0.
        maximum_validator_text (CharField): Maximum value validator text.
        minimum_validator_column (PositiveSmallIntegerField): Index of the minimum value
            validator column, starting in 0.
        minimum_validator_text (CharField): Minimum value validator text.
        accumulate (PositiveSmallIntegerField): If set to a number of minutes, the data
            will be accumulated over that period.
        resolution (DecimalField): Resolution of the data. Only used if it is to be
            accumulated.
        incremental (BooleanField): Whether the data is an incremental counter. If it
            is, any value below the previous one will be removed.
        decimal_comma (BooleanField): Whether the data uses a comma as a decimal
            separator.
    """

    cls_id = models.AutoField("Id", primary_key=True, help_text="Primary key.")
    format = models.ForeignKey(
        Format,
        on_delete=models.PROTECT,
        verbose_name="Format",
        help_text="The format of the data file.",
    )
    variable = models.ForeignKey(
        Variable,
        on_delete=models.PROTECT,
        verbose_name="Variable",
        help_text="The variable to which the data belongs.",
    )
    value = models.PositiveSmallIntegerField(
        "Value column", help_text="Index of the value column, starting in 0."
    )
    maximum = models.PositiveSmallIntegerField(
        "Maximum value column",
        blank=True,
        null=True,
        help_text="Index of the maximum value column, starting in 0.",
    )
    minimum = models.PositiveSmallIntegerField(
        "Minimum value column",
        blank=True,
        null=True,
        help_text="Index of the minimum value column, starting in 0.",
    )
    value_validator_column = models.PositiveSmallIntegerField(
        "Value validator column",
        blank=True,
        null=True,
        help_text="Index of the value validator column, starting in 0.",
    )
    value_validator_text = models.CharField(
        "Value validator text",
        max_length=10,
        blank=True,
        null=True,
        help_text="Value validator text.",
    )
    maximum_validator_column = models.PositiveSmallIntegerField(
        "Maximum value validator column",
        blank=True,
        null=True,
        help_text="Index of the maximum value validator column, starting in 0.",
    )
    maximum_validator_text = models.CharField(
        "Maximum value validator text",
        max_length=10,
        blank=True,
        null=True,
        help_text="Maximum value validator text.",
    )
    minimum_validator_column = models.PositiveSmallIntegerField(
        "Minimum value validator column",
        blank=True,
        null=True,
        help_text="Index of the minimum value validator column, starting in 0.",
    )
    minimum_validator_text = models.CharField(
        "Minimum value validator text",
        max_length=10,
        blank=True,
        null=True,
        help_text="Minimum value validator text.",
    )
    accumulate = models.PositiveSmallIntegerField(
        "Accumulate minutes",
        null=True,
        blank=True,
        help_text="When set to a number of minutes, the data will be accumulated over"
        " that period.",
        validators=[MinValueValidator(1)],
    )
    resolution = models.DecimalField(
        "Resolution",
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Resolution of the data. Only used if it is to be accumulated.",
        validators=[
            MinValueValidator(0.01)  # Smallest positive number with 2 decimals
        ],
    )
    incremental = models.BooleanField(
        "Is it an incremental counter?",
        default=False,
        help_text="Whether the data is an incremental counter. If it is, any value"
        " below the previous one will be removed.",
    )
    decimal_comma = models.BooleanField(
        "Uses comma as decimal separator?",
        default=False,
        help_text="Whether the data uses a comma as a decimal separator.",
    )

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return str(self.cls_id)

    def get_absolute_url(self) -> str:
        """Get the absolute URL of the object."""
        return reverse("formatting:classification_detail", kwargs={"pk": self.pk})

    def clean(self) -> None:
        """Validate the model instance.

        It checks that the column indices are different, and that the accumulation
        period is greater than zero if it is set. It also checks that the resolution is
        set if the data is accumulated.
        """
        if self.accumulate and self.resolution is None:
            raise ValidationError(
                {"resolution": "The resolution must be set if the data is accumulated."}
            )

        col_names = [
            "value",
            "maximum",
            "minimum",
            "value_validator_column",
            "maximum_validator_column",
            "minimum_validator_column",
        ]
        unique = defaultdict(list)
        for name in col_names:
            if getattr(self, name) is not None:
                unique[getattr(self, name)].append(name)
        for _, names in unique.items():
            if len(names) != 1:
                msg = "The columns must be different."
                raise ValidationError({field: msg for field in names})

    class Meta:
        ordering = ("variable",)
