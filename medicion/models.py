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

from typing import NamedTuple

from django.db import models
from django.urls import reverse

from station.models import Station


class PermissionsMeasurement(models.Model):
    """
    Model used to define the permission "validar".
    """

    class Meta:
        managed = False
        default_permissions = ()
        permissions = (("validar", "usar interfaz de validación"),)


class PolarWind(models.Model):
    date = models.DateTimeField("Date")
    speed = models.DecimalField("Speed", max_digits=14, decimal_places=6, null=True)
    direction = models.DecimalField(
        "Direction", max_digits=14, decimal_places=6, null=True
    )

    class Meta:
        """
        Para que no se cree en la migracion.

        NOTE: Why don't we want this in the migration?
        """

        default_permissions = ()
        managed = False


class FlowThroughStation(models.Model):
    """
    Flow (of water) through the station.
    """

    id = models.AutoField("Id", primary_key=True)
    station = models.ForeignKey(
        Station, models.SET_NULL, blank=True, null=True, verbose_name="Station"
    )
    start_date = models.DateTimeField("Start date")
    end_date = models.DateTimeField("End date")
    value = models.DecimalField(
        "Value", max_digits=14, decimal_places=6, blank=True, null=True
    )
    calibration_sensor_strip = models.NullBooleanField("Calibration", default=False)


class DischargeCurve(models.Model):
    """
    NOTE: No idea what this is -> Ask Pablo
    """

    id = models.AutoField("Id", primary_key=True)
    station = models.ForeignKey(
        Station, on_delete=models.SET_NULL, null=True, verbose_name="Station"
    )
    date = models.DateTimeField("Date")
    require_recalculate_flow = models.BooleanField(
        verbose_name="Requires re-calculate flow?", default=False
    )

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse("medicion:dischargecurve_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("station", "date")
        unique_together = ("station", "date")


class LevelFunction(models.Model):
    """
    NOTE: No idea what this is -> Ask Pablo
    """

    discharge_curve = models.ForeignKey(DischargeCurve, on_delete=models.CASCADE)
    level = models.DecimalField(
        "Level (cm)", max_digits=5, decimal_places=1, db_index=True
    )
    function = models.CharField("Function", max_length=80)

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("medicion:levelfunction_detail", kwargs={"pk": self.pk})

    class Meta:
        default_permissions = ()
        ordering = (
            "discharge_curve",
            "level",
        )


class CursorDbclima(models.Model):
    """
    NOTE: No idea what this is -> Ask Pablo
    """

    station_id = models.IntegerField(primary_key=True)
    date = models.DateTimeField(null=True)


class CursorEmaaphidro(models.Model):
    """
    NOTE: No idea what this is -> Ask Pablo
    """

    station_id_paramh2o = models.IntegerField(primary_key=True)
    station_id_emaaphidro = models.SmallIntegerField()
    station_code = models.CharField(max_length=4)
    date = models.DateTimeField()


##############################################################


class BaseMeasurement(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    station_id = models.PositiveIntegerField("station_id")
    date = models.DateTimeField("Date")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "date"]),
            models.Index(fields=["date", "station_id"]),
        ]


def limits_model(
    num, max_digits=14, decimal_places=6, value=True, maximum=True, minimum=True
) -> models.Model:
    fields = {}
    if value:
        fields["value"] = models.DecimalField(
            "Value",
            max_digits=max_digits,
            decimal_places=decimal_places,
            null=True,
        )
    if maximum:
        fields["maximum"] = models.DecimalField(
            "Maximum",
            max_digits=max_digits,
            decimal_places=decimal_places,
            null=True,
        )
    if minimum:
        fields["minimum"] = models.DecimalField(
            "Minimum",
            max_digits=max_digits,
            decimal_places=decimal_places,
            null=True,
        )
    return type(f"Limits{num}", (models.Model,), fields)


class Var1Measurement(
    BaseMeasurement,
    limits_model(1, max_digits=6, decimal_places=2, maximum=False, minimum=False),
):
    pass


class Var2Measurement(BaseMeasurement, limits_model(2, max_digits=5, decimal_places=2)):
    pass


class Var3Measurement(BaseMeasurement, limits_model(3)):
    pass


class Var4Measurement(BaseMeasurement, limits_model(4)):
    pass


class Var5Measurement(BaseMeasurement, limits_model(5)):
    pass


class Var6Measurement(BaseMeasurement, limits_model(6)):
    pass


class Var7Measurement(BaseMeasurement, limits_model(7)):
    pass


class Var8Measurement(BaseMeasurement, limits_model(8)):
    pass


class Var9Measurement(BaseMeasurement, limits_model(9)):
    pass


class Var10Measurement(BaseMeasurement, limits_model(10)):
    pass


class Var11Measurement(BaseMeasurement, limits_model(11)):
    pass


class Var12Measurement(BaseMeasurement, limits_model(12)):
    pass


class Var13Measurement(BaseMeasurement, limits_model(13, maximum=False, minimum=False)):
    pass


class Var14Measurement(BaseMeasurement, limits_model(14, maximum=False, minimum=False)):
    fecha_importacion = models.DateTimeField("Date Importación")
    fecha_inicio = models.DateTimeField("Date inicio datos")
    calibrado = models.BooleanField("Calibrado")
    incertidumbre = models.DecimalField(
        "Incertidumbre",
        max_digits=DigVar.v14.max_digits,
        decimal_places=DigVar.v14.decimal_places,
        null=True,
    )
    comentario = models.CharField("Comentario", null=True, max_length=250)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "fecha_importacion"]),
            models.Index(fields=["station_id", "fecha_inicio", "date"]),
            models.Index(fields=["fecha_importacion"]),
        ]


class Var15Measurement(BaseMeasurement, limits_model(15)):
    pass


class Var16Measurement(BaseMeasurement, limits_model(16)):
    pass


class Var17Measurement(BaseMeasurement, limits_model(17)):
    pass


class Var18Measurement(BaseMeasurement, limits_model(18)):
    pass


class Var19Measurement(BaseMeasurement, limits_model(19)):
    pass


class Var20Measurement(BaseMeasurement, limits_model(20)):
    pass


class Var21Measurement(BaseMeasurement, limits_model(21)):
    pass


class Var22Measurement(BaseMeasurement, limits_model(22)):
    pass


class Var23Measurement(BaseMeasurement, limits_model(23)):
    pass


class Var24Measurement(BaseMeasurement, limits_model(24)):
    pass


# Variables creadas para boya con diferentes depthes


class Var101Measurement(
    BaseMeasurement,
    limits_model(101, max_digits=6, decimal_places=2, maximum=False, minimum=False),
):
    """
    Temperatura agua
        Depth en centimetros
        Unidad : grados Celcius
    """

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "date"]),
        ]


class Var102Measurement(
    BaseMeasurement,
    limits_model(102, max_digits=6, decimal_places=2, maximum=False, minimum=False),
):
    """
    pH Acidez agua
        Depth en centimetros
        Unidad : pH
    """

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "date"]),
        ]


class Var103Measurement(
    BaseMeasurement,
    limits_model(103, max_digits=6, decimal_places=2, maximum=False, minimum=False),
):
    """
    ORP : Potencial REDOX en agua
        Depth en centimetros
        Unidad : mV
    """

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "date"]),
        ]


class Var104Measurement(
    BaseMeasurement,
    limits_model(104, max_digits=6, decimal_places=2, maximum=False, minimum=False),
):
    """
    Turp Turbidez en agua
        Depth en centimetros
        Unidad : NTU
    """

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "date"]),
        ]


class Var105Measurement(
    BaseMeasurement,
    limits_model(105, max_digits=6, decimal_places=2, maximum=False, minimum=False),
):
    """
    Chl : Concentracion Cloro
        Depth en centimetros
        Unidad : ug/l
    """

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "date"]),
        ]


class Var106Measurement(
    BaseMeasurement,
    limits_model(106, max_digits=6, decimal_places=2, maximum=False, minimum=False),
):
    """
    HDO : Oxígeno disuelto en agua
        Depth en centimetros
        Unidad : mg/l
    """

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "date"]),
        ]


class Var107Measurement(
    BaseMeasurement,
    limits_model(107, max_digits=6, decimal_places=2, maximum=False, minimum=False),
):
    """
    % HDO : Porcentaje Oxígeno disuelto en agua
        Depth en centimetros
        Unidad : mg/l
    """

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "date"]),
        ]


class Var108Measurement(
    BaseMeasurement,
    limits_model(108, max_digits=6, decimal_places=2, maximum=False, minimum=False),
):
    """
    BGAPC : Ficocianina
        Depth en centimetros
        Unidad :
    """

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "date"]),
        ]
