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

from medicion.models import DigVar

## Models here link a station (id), date, value (medicion.models.DigVar).
## Most also have max, min (DigVar).
## Var1Diario and Var10Diario are used in indices.functions. These relate
## to the key variables of precipitation and flow.
## The rest are unused.


class Var1Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=(DigVar.v1.max_digits + 1),
        decimal_places=DigVar.v1.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var2Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v2.max_digits + 1,
        decimal_places=DigVar.v2.decimal_places + 1,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v2.max_digits,
        decimal_places=DigVar.v2.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v2.max_digits,
        decimal_places=DigVar.v2.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v2.max_digits,
        decimal_places=DigVar.v2.decimal_places + 1,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v2.max_digits,
        decimal_places=DigVar.v2.decimal_places + 1,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var3Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v3.max_digits,
        decimal_places=DigVar.v3.decimal_places,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v3.max_digits,
        decimal_places=DigVar.v3.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v3.max_digits,
        decimal_places=DigVar.v3.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v3.max_digits,
        decimal_places=DigVar.v3.decimal_places,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v3.max_digits,
        decimal_places=DigVar.v3.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var4Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v4.max_digits,
        decimal_places=DigVar.v4.decimal_places,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v4.max_digits,
        decimal_places=DigVar.v4.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v4.max_digits,
        decimal_places=DigVar.v4.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v4.max_digits,
        decimal_places=DigVar.v4.decimal_places,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v4.max_digits,
        decimal_places=DigVar.v4.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var5Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v5.max_digits,
        decimal_places=DigVar.v5.decimal_places,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v5.max_digits,
        decimal_places=DigVar.v5.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v5.max_digits,
        decimal_places=DigVar.v5.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v5.max_digits,
        decimal_places=DigVar.v5.decimal_places,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v5.max_digits,
        decimal_places=DigVar.v5.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var6Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v6.max_digits,
        decimal_places=DigVar.v6.decimal_places,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v6.max_digits,
        decimal_places=DigVar.v6.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v6.max_digits,
        decimal_places=DigVar.v6.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v6.max_digits,
        decimal_places=DigVar.v6.decimal_places,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v6.max_digits,
        decimal_places=DigVar.v6.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var7Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v7.max_digits,
        decimal_places=DigVar.v7.decimal_places,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v7.max_digits,
        decimal_places=DigVar.v7.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v7.max_digits,
        decimal_places=DigVar.v7.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v7.max_digits,
        decimal_places=DigVar.v7.decimal_places,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v7.max_digits,
        decimal_places=DigVar.v7.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var8Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v8.max_digits,
        decimal_places=DigVar.v8.decimal_places,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v8.max_digits,
        decimal_places=DigVar.v8.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v8.max_digits,
        decimal_places=DigVar.v8.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v8.max_digits,
        decimal_places=DigVar.v8.decimal_places,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v8.max_digits,
        decimal_places=DigVar.v8.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var9Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v9.max_digits,
        decimal_places=DigVar.v9.decimal_places,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v9.max_digits,
        decimal_places=DigVar.v9.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v9.max_digits,
        decimal_places=DigVar.v9.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v9.max_digits,
        decimal_places=DigVar.v9.decimal_places,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v9.max_digits,
        decimal_places=DigVar.v9.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var10Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v10.max_digits,
        decimal_places=DigVar.v10.decimal_places,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v10.max_digits,
        decimal_places=DigVar.v10.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v10.max_digits,
        decimal_places=DigVar.v10.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v10.max_digits,
        decimal_places=DigVar.v10.decimal_places,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v10.max_digits,
        decimal_places=DigVar.v10.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var11Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v11.max_digits,
        decimal_places=DigVar.v11.decimal_places,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v11.max_digits,
        decimal_places=DigVar.v11.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v11.max_digits,
        decimal_places=DigVar.v11.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v11.max_digits,
        decimal_places=DigVar.v11.decimal_places,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v11.max_digits,
        decimal_places=DigVar.v11.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var12Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v12.max_digits,
        decimal_places=DigVar.v12.decimal_places,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v12.max_digits,
        decimal_places=DigVar.v12.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v12.max_digits,
        decimal_places=DigVar.v12.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v12.max_digits,
        decimal_places=DigVar.v12.decimal_places,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v12.max_digits,
        decimal_places=DigVar.v12.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var13Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v13.max_digits,
        decimal_places=DigVar.v13.decimal_places,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v13.max_digits,
        decimal_places=DigVar.v13.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v13.max_digits,
        decimal_places=DigVar.v13.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v13.max_digits,
        decimal_places=DigVar.v13.decimal_places,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v13.max_digits,
        decimal_places=DigVar.v13.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var14Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v14.max_digits,
        decimal_places=DigVar.v14.decimal_places,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v14.max_digits,
        decimal_places=DigVar.v14.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v14.max_digits,
        decimal_places=DigVar.v14.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v14.max_digits,
        decimal_places=DigVar.v14.decimal_places,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v14.max_digits,
        decimal_places=DigVar.v14.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var15Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v15.max_digits,
        decimal_places=DigVar.v15.decimal_places,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v15.max_digits,
        decimal_places=DigVar.v15.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v15.max_digits,
        decimal_places=DigVar.v15.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v15.max_digits,
        decimal_places=DigVar.v15.decimal_places,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v15.max_digits,
        decimal_places=DigVar.v15.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var16Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v16.max_digits,
        decimal_places=DigVar.v16.decimal_places,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v16.max_digits,
        decimal_places=DigVar.v16.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v16.max_digits,
        decimal_places=DigVar.v16.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v16.max_digits,
        decimal_places=DigVar.v16.decimal_places,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v16.max_digits,
        decimal_places=DigVar.v16.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var17Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v17.max_digits,
        decimal_places=DigVar.v17.decimal_places,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v17.max_digits,
        decimal_places=DigVar.v17.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v17.max_digits,
        decimal_places=DigVar.v17.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v17.max_digits,
        decimal_places=DigVar.v17.decimal_places,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v17.max_digits,
        decimal_places=DigVar.v17.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var18Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v18.max_digits,
        decimal_places=DigVar.v18.decimal_places,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v18.max_digits,
        decimal_places=DigVar.v18.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v18.max_digits,
        decimal_places=DigVar.v18.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v18.max_digits,
        decimal_places=DigVar.v18.decimal_places,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v18.max_digits,
        decimal_places=DigVar.v18.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var19Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v19.max_digits,
        decimal_places=DigVar.v19.decimal_places,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v19.max_digits,
        decimal_places=DigVar.v19.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v19.max_digits,
        decimal_places=DigVar.v19.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v19.max_digits,
        decimal_places=DigVar.v19.decimal_places,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v19.max_digits,
        decimal_places=DigVar.v19.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var20Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v20.max_digits,
        decimal_places=DigVar.v20.decimal_places,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v20.max_digits,
        decimal_places=DigVar.v20.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v20.max_digits,
        decimal_places=DigVar.v20.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v20.max_digits,
        decimal_places=DigVar.v20.decimal_places,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v20.max_digits,
        decimal_places=DigVar.v20.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var21Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v21.max_digits,
        decimal_places=DigVar.v21.decimal_places,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v21.max_digits,
        decimal_places=DigVar.v21.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v21.max_digits,
        decimal_places=DigVar.v21.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v21.max_digits,
        decimal_places=DigVar.v21.decimal_places,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v21.max_digits,
        decimal_places=DigVar.v21.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var22Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v22.max_digits,
        decimal_places=DigVar.v22.decimal_places,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v22.max_digits,
        decimal_places=DigVar.v22.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v22.max_digits,
        decimal_places=DigVar.v22.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v22.max_digits,
        decimal_places=DigVar.v22.decimal_places,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v22.max_digits,
        decimal_places=DigVar.v22.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var23Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v23.max_digits,
        decimal_places=DigVar.v23.decimal_places,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v23.max_digits,
        decimal_places=DigVar.v23.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v23.max_digits,
        decimal_places=DigVar.v23.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v23.max_digits,
        decimal_places=DigVar.v23.decimal_places,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v23.max_digits,
        decimal_places=DigVar.v23.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


class Var24Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v24.max_digits,
        decimal_places=DigVar.v24.decimal_places,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v24.max_digits,
        decimal_places=DigVar.v24.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v24.max_digits,
        decimal_places=DigVar.v24.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v24.max_digits,
        decimal_places=DigVar.v24.decimal_places,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v24.max_digits,
        decimal_places=DigVar.v24.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
            models.Index(fields=["fecha", "estacion_id"]),
        ]
        default_permissions = ()


#############################################


class Var101Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v101.max_digits + 1,
        decimal_places=DigVar.v101.decimal_places + 1,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v101.max_digits,
        decimal_places=DigVar.v101.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v101.max_digits,
        decimal_places=DigVar.v101.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v101.max_digits + 1,
        decimal_places=DigVar.v101.decimal_places + 1,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v101.max_digits + 1,
        decimal_places=DigVar.v101.decimal_places + 1,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "profundidad", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
        ]
        default_permissions = ()


class Var102Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v102.max_digits + 1,
        decimal_places=DigVar.v102.decimal_places + 1,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v102.max_digits,
        decimal_places=DigVar.v102.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v102.max_digits,
        decimal_places=DigVar.v102.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v102.max_digits + 1,
        decimal_places=DigVar.v102.decimal_places + 1,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v102.max_digits + 1,
        decimal_places=DigVar.v102.decimal_places + 1,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "profundidad", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
        ]
        default_permissions = ()


class Var103Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v103.max_digits + 1,
        decimal_places=DigVar.v103.decimal_places + 1,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v103.max_digits,
        decimal_places=DigVar.v103.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v103.max_digits,
        decimal_places=DigVar.v103.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v103.max_digits + 1,
        decimal_places=DigVar.v103.decimal_places + 1,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v103.max_digits + 1,
        decimal_places=DigVar.v103.decimal_places + 1,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "profundidad", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
        ]
        default_permissions = ()


class Var104Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v104.max_digits + 1,
        decimal_places=DigVar.v104.decimal_places + 1,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v104.max_digits,
        decimal_places=DigVar.v104.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v104.max_digits,
        decimal_places=DigVar.v104.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v104.max_digits + 1,
        decimal_places=DigVar.v104.decimal_places + 1,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v104.max_digits + 1,
        decimal_places=DigVar.v104.decimal_places + 1,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "profundidad", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
        ]
        default_permissions = ()


class Var105Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v105.max_digits + 1,
        decimal_places=DigVar.v105.decimal_places + 1,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v105.max_digits,
        decimal_places=DigVar.v105.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v105.max_digits,
        decimal_places=DigVar.v105.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v105.max_digits + 1,
        decimal_places=DigVar.v105.decimal_places + 1,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v105.max_digits + 1,
        decimal_places=DigVar.v105.decimal_places + 1,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "profundidad", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
        ]
        default_permissions = ()


class Var106Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v106.max_digits + 1,
        decimal_places=DigVar.v106.decimal_places + 1,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v106.max_digits,
        decimal_places=DigVar.v106.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v106.max_digits,
        decimal_places=DigVar.v106.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v106.max_digits + 1,
        decimal_places=DigVar.v106.decimal_places + 1,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v106.max_digits + 1,
        decimal_places=DigVar.v106.decimal_places + 1,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "profundidad", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
        ]
        default_permissions = ()


class Var107Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v107.max_digits + 1,
        decimal_places=DigVar.v107.decimal_places + 1,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v107.max_digits,
        decimal_places=DigVar.v107.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v107.max_digits,
        decimal_places=DigVar.v107.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v107.max_digits + 1,
        decimal_places=DigVar.v107.decimal_places + 1,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v107.max_digits + 1,
        decimal_places=DigVar.v107.decimal_places + 1,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "profundidad", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
        ]
        default_permissions = ()


class Var108Diario(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v108.max_digits + 1,
        decimal_places=DigVar.v108.decimal_places + 1,
        null=True,
    )
    max_abs = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v108.max_digits,
        decimal_places=DigVar.v108.decimal_places,
        null=True,
    )
    min_abs = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v108.max_digits,
        decimal_places=DigVar.v108.decimal_places,
        null=True,
    )
    max_del_prom = models.DecimalField(
        "Máximo del promedio",
        max_digits=DigVar.v108.max_digits + 1,
        decimal_places=DigVar.v108.decimal_places + 1,
        null=True,
    )
    min_del_prom = models.DecimalField(
        "Mínimo del promedio",
        max_digits=DigVar.v108.max_digits + 1,
        decimal_places=DigVar.v108.decimal_places + 1,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ("estacion_id", "profundidad", "fecha")
        indexes = [
            models.Index(fields=["usado_para_mensual", "id"]),
        ]
        default_permissions = ()
