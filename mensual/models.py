################################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos (iMHEA)
# basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#         Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS), Ecuador.
#         Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones creadoras,
#              ya sea en uso total o parcial del código.

from django.db import models

from estacion.models import Estacion
from medicion.models import DigVar


class Var1Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=(DigVar.v1.max_dig + 2),
        decimal_places=DigVar.v1.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_anual = models.BooleanField("Usado para anual", default=False, null=True)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_anual"]),
        ]


class Var2Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v2.max_dig + 1,
        decimal_places=DigVar.v2.dec_pla + 1,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v2.max_dig,
        decimal_places=DigVar.v2.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v2.max_dig,
        decimal_places=DigVar.v2.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v2.max_dig,
        decimal_places=DigVar.v2.dec_pla + 1,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v2.max_dig,
        decimal_places=DigVar.v2.dec_pla + 1,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


class Var3Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v3.max_dig,
        decimal_places=DigVar.v3.dec_pla,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v3.max_dig,
        decimal_places=DigVar.v3.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v3.max_dig,
        decimal_places=DigVar.v3.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v3.max_dig,
        decimal_places=DigVar.v3.dec_pla,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v3.max_dig,
        decimal_places=DigVar.v3.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


class Var4Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v4.max_dig,
        decimal_places=DigVar.v4.dec_pla,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v4.max_dig,
        decimal_places=DigVar.v4.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v4.max_dig,
        decimal_places=DigVar.v4.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v4.max_dig,
        decimal_places=DigVar.v4.dec_pla,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v4.max_dig,
        decimal_places=DigVar.v4.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


class Var5Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v5.max_dig,
        decimal_places=DigVar.v5.dec_pla,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v5.max_dig,
        decimal_places=DigVar.v5.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v5.max_dig,
        decimal_places=DigVar.v5.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v5.max_dig,
        decimal_places=DigVar.v5.dec_pla,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v5.max_dig,
        decimal_places=DigVar.v5.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


class Var6Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v6.max_dig,
        decimal_places=DigVar.v6.dec_pla,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v6.max_dig,
        decimal_places=DigVar.v6.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v6.max_dig,
        decimal_places=DigVar.v6.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v6.max_dig,
        decimal_places=DigVar.v6.dec_pla,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v6.max_dig,
        decimal_places=DigVar.v6.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


class Var7Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v7.max_dig,
        decimal_places=DigVar.v7.dec_pla,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v7.max_dig,
        decimal_places=DigVar.v7.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v7.max_dig,
        decimal_places=DigVar.v7.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v7.max_dig,
        decimal_places=DigVar.v7.dec_pla,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v7.max_dig,
        decimal_places=DigVar.v7.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


class Var8Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v8.max_dig,
        decimal_places=DigVar.v8.dec_pla,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v8.max_dig,
        decimal_places=DigVar.v8.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v8.max_dig,
        decimal_places=DigVar.v8.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v8.max_dig,
        decimal_places=DigVar.v8.dec_pla,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v8.max_dig,
        decimal_places=DigVar.v8.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


class Var9Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v9.max_dig,
        decimal_places=DigVar.v9.dec_pla,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v9.max_dig,
        decimal_places=DigVar.v9.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v9.max_dig,
        decimal_places=DigVar.v9.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v9.max_dig,
        decimal_places=DigVar.v9.dec_pla,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v9.max_dig,
        decimal_places=DigVar.v9.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


class Var10Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v10.max_dig,
        decimal_places=DigVar.v10.dec_pla,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v10.max_dig,
        decimal_places=DigVar.v10.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v10.max_dig,
        decimal_places=DigVar.v10.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v10.max_dig,
        decimal_places=DigVar.v10.dec_pla,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v10.max_dig,
        decimal_places=DigVar.v10.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


class Var11Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v11.max_dig,
        decimal_places=DigVar.v11.dec_pla,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v11.max_dig,
        decimal_places=DigVar.v11.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v11.max_dig,
        decimal_places=DigVar.v11.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v11.max_dig,
        decimal_places=DigVar.v11.dec_pla,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v11.max_dig,
        decimal_places=DigVar.v11.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


class Var12Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v12.max_dig,
        decimal_places=DigVar.v12.dec_pla,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v12.max_dig,
        decimal_places=DigVar.v12.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v12.max_dig,
        decimal_places=DigVar.v12.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v12.max_dig,
        decimal_places=DigVar.v12.dec_pla,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v12.max_dig,
        decimal_places=DigVar.v12.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


class Var13Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v13.max_dig,
        decimal_places=DigVar.v13.dec_pla,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v13.max_dig,
        decimal_places=DigVar.v13.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v13.max_dig,
        decimal_places=DigVar.v13.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v13.max_dig,
        decimal_places=DigVar.v13.dec_pla,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v13.max_dig,
        decimal_places=DigVar.v13.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


class Var14Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v14.max_dig,
        decimal_places=DigVar.v14.dec_pla,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v14.max_dig,
        decimal_places=DigVar.v14.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v14.max_dig,
        decimal_places=DigVar.v14.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v14.max_dig,
        decimal_places=DigVar.v14.dec_pla,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v14.max_dig,
        decimal_places=DigVar.v14.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


class Var15Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v15.max_dig,
        decimal_places=DigVar.v15.dec_pla,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v15.max_dig,
        decimal_places=DigVar.v15.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v15.max_dig,
        decimal_places=DigVar.v15.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v15.max_dig,
        decimal_places=DigVar.v15.dec_pla,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v15.max_dig,
        decimal_places=DigVar.v15.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


class Var16Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v16.max_dig,
        decimal_places=DigVar.v16.dec_pla,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v16.max_dig,
        decimal_places=DigVar.v16.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v16.max_dig,
        decimal_places=DigVar.v16.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v16.max_dig,
        decimal_places=DigVar.v16.dec_pla,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v16.max_dig,
        decimal_places=DigVar.v16.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


class Var17Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v17.max_dig,
        decimal_places=DigVar.v17.dec_pla,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v17.max_dig,
        decimal_places=DigVar.v17.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v17.max_dig,
        decimal_places=DigVar.v17.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v17.max_dig,
        decimal_places=DigVar.v17.dec_pla,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v17.max_dig,
        decimal_places=DigVar.v17.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


class Var18Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v18.max_dig,
        decimal_places=DigVar.v18.dec_pla,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v18.max_dig,
        decimal_places=DigVar.v18.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v18.max_dig,
        decimal_places=DigVar.v18.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v18.max_dig,
        decimal_places=DigVar.v18.dec_pla,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v18.max_dig,
        decimal_places=DigVar.v18.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


class Var19Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v19.max_dig,
        decimal_places=DigVar.v19.dec_pla,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v19.max_dig,
        decimal_places=DigVar.v19.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v19.max_dig,
        decimal_places=DigVar.v19.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v19.max_dig,
        decimal_places=DigVar.v19.dec_pla,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v19.max_dig,
        decimal_places=DigVar.v19.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


class Var20Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v20.max_dig,
        decimal_places=DigVar.v20.dec_pla,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v20.max_dig,
        decimal_places=DigVar.v20.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v20.max_dig,
        decimal_places=DigVar.v20.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v20.max_dig,
        decimal_places=DigVar.v20.dec_pla,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v20.max_dig,
        decimal_places=DigVar.v20.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


class Var21Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v21.max_dig,
        decimal_places=DigVar.v21.dec_pla,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v21.max_dig,
        decimal_places=DigVar.v21.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v21.max_dig,
        decimal_places=DigVar.v21.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v21.max_dig,
        decimal_places=DigVar.v21.dec_pla,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v21.max_dig,
        decimal_places=DigVar.v21.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


class Var22Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v22.max_dig,
        decimal_places=DigVar.v22.dec_pla,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v22.max_dig,
        decimal_places=DigVar.v22.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v22.max_dig,
        decimal_places=DigVar.v22.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v22.max_dig,
        decimal_places=DigVar.v22.dec_pla,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v22.max_dig,
        decimal_places=DigVar.v22.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


class Var23Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v23.max_dig,
        decimal_places=DigVar.v23.dec_pla,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v23.max_dig,
        decimal_places=DigVar.v23.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v23.max_dig,
        decimal_places=DigVar.v23.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v23.max_dig,
        decimal_places=DigVar.v23.dec_pla,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v23.max_dig,
        decimal_places=DigVar.v23.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


class Var24Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v24.max_dig,
        decimal_places=DigVar.v24.dec_pla,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v24.max_dig,
        decimal_places=DigVar.v24.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v24.max_dig,
        decimal_places=DigVar.v24.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v24.max_dig,
        decimal_places=DigVar.v24.dec_pla,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v24.max_dig,
        decimal_places=DigVar.v24.dec_pla,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]


######################################################


class Var101Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v101.max_dig + 1,
        decimal_places=DigVar.v101.dec_pla + 1,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v101.max_dig,
        decimal_places=DigVar.v101.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v101.max_dig,
        decimal_places=DigVar.v101.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v101.max_dig + 1,
        decimal_places=DigVar.v101.dec_pla + 1,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v101.max_dig + 1,
        decimal_places=DigVar.v101.dec_pla + 1,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "profundidad", "fecha")


class Var102Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v102.max_dig + 1,
        decimal_places=DigVar.v102.dec_pla + 1,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v102.max_dig,
        decimal_places=DigVar.v102.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v102.max_dig,
        decimal_places=DigVar.v102.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v102.max_dig + 1,
        decimal_places=DigVar.v102.dec_pla + 1,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v102.max_dig + 1,
        decimal_places=DigVar.v102.dec_pla + 1,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "profundidad", "fecha")


class Var103Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v103.max_dig + 1,
        decimal_places=DigVar.v103.dec_pla + 1,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v103.max_dig,
        decimal_places=DigVar.v103.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v103.max_dig,
        decimal_places=DigVar.v103.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v103.max_dig + 1,
        decimal_places=DigVar.v103.dec_pla + 1,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v103.max_dig + 1,
        decimal_places=DigVar.v103.dec_pla + 1,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "profundidad", "fecha")


class Var104Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v104.max_dig + 1,
        decimal_places=DigVar.v104.dec_pla + 1,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v104.max_dig,
        decimal_places=DigVar.v104.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v104.max_dig,
        decimal_places=DigVar.v104.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v104.max_dig + 1,
        decimal_places=DigVar.v104.dec_pla + 1,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v104.max_dig + 1,
        decimal_places=DigVar.v104.dec_pla + 1,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "profundidad", "fecha")


class Var105Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v105.max_dig + 1,
        decimal_places=DigVar.v105.dec_pla + 1,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v105.max_dig,
        decimal_places=DigVar.v105.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v105.max_dig,
        decimal_places=DigVar.v105.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v105.max_dig + 1,
        decimal_places=DigVar.v105.dec_pla + 1,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v105.max_dig + 1,
        decimal_places=DigVar.v105.dec_pla + 1,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "profundidad", "fecha")


class Var106Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v106.max_dig + 1,
        decimal_places=DigVar.v106.dec_pla + 1,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v106.max_dig,
        decimal_places=DigVar.v106.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v106.max_dig,
        decimal_places=DigVar.v106.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v106.max_dig + 1,
        decimal_places=DigVar.v106.dec_pla + 1,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v106.max_dig + 1,
        decimal_places=DigVar.v106.dec_pla + 1,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "profundidad", "fecha")


class Var107Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v107.max_dig + 1,
        decimal_places=DigVar.v107.dec_pla + 1,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v107.max_dig,
        decimal_places=DigVar.v107.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v107.max_dig,
        decimal_places=DigVar.v107.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v107.max_dig + 1,
        decimal_places=DigVar.v107.dec_pla + 1,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v107.max_dig + 1,
        decimal_places=DigVar.v107.dec_pla + 1,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "profundidad", "fecha")


class Var108Mensual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v108.max_dig + 1,
        decimal_places=DigVar.v108.dec_pla + 1,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v108.max_dig,
        decimal_places=DigVar.v108.dec_pla,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v108.max_dig,
        decimal_places=DigVar.v108.dec_pla,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v108.max_dig + 1,
        decimal_places=DigVar.v108.dec_pla + 1,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v108.max_dig + 1,
        decimal_places=DigVar.v108.dec_pla + 1,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "profundidad", "fecha")
