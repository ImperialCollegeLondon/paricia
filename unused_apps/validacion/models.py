# -*- coding: utf-8 -*-

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

from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

from estacion.models import Estacion
from medicion.models import DigVar
from variable.models import Variable


class PermisosValidacion(models.Model):
    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            (
                "hidro_o_calidad_enviar_validacion",
                "Requerido para enviar la validación Hidro o Calidad",
            ),
            ("hidro_validar", "Hidro: validar"),
            ("hidro_borrar_solo_validados", "Hidro: borrar solo validados"),
            ("hidro_borrar_crudos_y_validados", "Hidro: borrar crudos y validados"),
            ("calidad_validar", "Calidad: Validar"),
        )


class Validacion(models.Model):
    val_id = models.AutoField("Id", primary_key=True)
    var_id = models.ForeignKey(
        Variable, models.SET_NULL, blank=True, null=True, verbose_name="Variable"
    )
    est_id = models.ForeignKey(
        Estacion, models.SET_NULL, blank=True, null=True, verbose_name="Estación"
    )
    fecha_validacion = models.DateField("Fecha validación")
    fecha_inicio_datos = models.DateTimeField("Fecha inicio datos")
    fecha_fin_datos = models.DateTimeField("Fecha fin datos")
    comentario = models.CharField("Comentario", max_length=350)

    def __str__(self):
        return (
            str(self.var_id)
            + " -- "
            + str(self.est_id)
            + " -- "
            + str(self.fecha_validacion)
        )

    def get_absolute_url(self):
        return reverse("validacion:validacion_index")

    class Meta:
        ordering = (
            "val_id",
            "est_id",
            "var_id",
        )
        indexes = [
            models.Index(fields=["var_id", "est_id"]),
        ]


########################################################################################################################
class ComentarioValidacion(models.Model):
    variable_id = models.SmallIntegerField(db_index=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    validado_id = models.PositiveIntegerField("Validación")
    comentario = models.CharField("Comentario", max_length=350)

    class Meta:
        indexes = [
            models.Index(fields=["variable_id", "estacion_id", "validado_id"]),
            models.Index(fields=["variable_id", "validado_id", "estacion_id"]),
            models.Index(fields=["estacion_id", "variable_id", "validado_id"]),
            models.Index(fields=["estacion_id", "validado_id", "variable_id"]),
            models.Index(fields=["validado_id", "estacion_id", "variable_id"]),
            models.Index(fields=["validado_id", "variable_id", "estacion_id"]),
        ]
        default_permissions = ()


class Var1Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v1.max_digits,
        decimal_places=DigVar.v1.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var2Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v2.max_digits,
        decimal_places=DigVar.v2.decimal_places,
        null=True,
    )
    maximo = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v2.max_digits,
        decimal_places=DigVar.v2.decimal_places,
        null=True,
    )
    minimo = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v2.max_digits,
        decimal_places=DigVar.v2.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var3Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v3.max_digits,
        decimal_places=DigVar.v3.decimal_places,
        null=True,
    )
    maximo = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v3.max_digits,
        decimal_places=DigVar.v3.decimal_places,
        null=True,
    )
    minimo = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v3.max_digits,
        decimal_places=DigVar.v3.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var4Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v4.max_digits,
        decimal_places=DigVar.v4.decimal_places,
        null=True,
    )
    maximo = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v4.max_digits,
        decimal_places=DigVar.v4.decimal_places,
        null=True,
    )
    minimo = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v4.max_digits,
        decimal_places=DigVar.v4.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var5Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v5.max_digits,
        decimal_places=DigVar.v5.decimal_places,
        null=True,
    )
    maximo = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v5.max_digits,
        decimal_places=DigVar.v5.decimal_places,
        null=True,
    )
    minimo = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v5.max_digits,
        decimal_places=DigVar.v5.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var6Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v6.max_digits,
        decimal_places=DigVar.v6.decimal_places,
        null=True,
    )
    maximo = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v6.max_digits,
        decimal_places=DigVar.v6.decimal_places,
        null=True,
    )
    minimo = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v6.max_digits,
        decimal_places=DigVar.v6.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var7Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v7.max_digits,
        decimal_places=DigVar.v7.decimal_places,
        null=True,
    )
    maximo = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v7.max_digits,
        decimal_places=DigVar.v7.decimal_places,
        null=True,
    )
    minimo = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v7.max_digits,
        decimal_places=DigVar.v7.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var8Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v8.max_digits,
        decimal_places=DigVar.v8.decimal_places,
        null=True,
    )
    maximo = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v8.max_digits,
        decimal_places=DigVar.v8.decimal_places,
        null=True,
    )
    minimo = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v8.max_digits,
        decimal_places=DigVar.v8.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var9Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v9.max_digits,
        decimal_places=DigVar.v9.decimal_places,
        null=True,
    )
    maximo = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v9.max_digits,
        decimal_places=DigVar.v9.decimal_places,
        null=True,
    )
    minimo = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v9.max_digits,
        decimal_places=DigVar.v9.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var10Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v10.max_digits,
        decimal_places=DigVar.v10.decimal_places,
        null=True,
    )
    maximo = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v10.max_digits,
        decimal_places=DigVar.v10.decimal_places,
        null=True,
    )
    minimo = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v10.max_digits,
        decimal_places=DigVar.v10.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var11Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v11.max_digits,
        decimal_places=DigVar.v11.decimal_places,
        null=True,
    )
    maximo = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v11.max_digits,
        decimal_places=DigVar.v11.decimal_places,
        null=True,
    )
    minimo = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v11.max_digits,
        decimal_places=DigVar.v11.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var12Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v12.max_digits,
        decimal_places=DigVar.v12.decimal_places,
        null=True,
    )
    maximo = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v12.max_digits,
        decimal_places=DigVar.v12.decimal_places,
        null=True,
    )
    minimo = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v12.max_digits,
        decimal_places=DigVar.v12.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var13Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v13.max_digits,
        decimal_places=DigVar.v13.decimal_places,
        null=True,
    )
    maximo = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v13.max_digits,
        decimal_places=DigVar.v13.decimal_places,
        null=True,
    )
    minimo = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v13.max_digits,
        decimal_places=DigVar.v13.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var14Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v14.max_digits,
        decimal_places=DigVar.v14.decimal_places,
        null=True,
    )
    maximo = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v14.max_digits,
        decimal_places=DigVar.v14.decimal_places,
        null=True,
    )
    minimo = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v14.max_digits,
        decimal_places=DigVar.v14.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var15Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v15.max_digits,
        decimal_places=DigVar.v15.decimal_places,
        null=True,
    )
    maximo = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v15.max_digits,
        decimal_places=DigVar.v15.decimal_places,
        null=True,
    )
    minimo = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v15.max_digits,
        decimal_places=DigVar.v15.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var16Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v16.max_digits,
        decimal_places=DigVar.v16.decimal_places,
        null=True,
    )
    maximo = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v16.max_digits,
        decimal_places=DigVar.v16.decimal_places,
        null=True,
    )
    minimo = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v16.max_digits,
        decimal_places=DigVar.v16.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var17Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v17.max_digits,
        decimal_places=DigVar.v17.decimal_places,
        null=True,
    )
    maximo = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v17.max_digits,
        decimal_places=DigVar.v17.decimal_places,
        null=True,
    )
    minimo = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v17.max_digits,
        decimal_places=DigVar.v17.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var18Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v18.max_digits,
        decimal_places=DigVar.v18.decimal_places,
        null=True,
    )
    maximo = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v18.max_digits,
        decimal_places=DigVar.v18.decimal_places,
        null=True,
    )
    minimo = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v18.max_digits,
        decimal_places=DigVar.v18.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var19Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v19.max_digits,
        decimal_places=DigVar.v19.decimal_places,
        null=True,
    )
    maximo = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v19.max_digits,
        decimal_places=DigVar.v19.decimal_places,
        null=True,
    )
    minimo = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v19.max_digits,
        decimal_places=DigVar.v19.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var20Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v20.max_digits,
        decimal_places=DigVar.v20.decimal_places,
        null=True,
    )
    maximo = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v20.max_digits,
        decimal_places=DigVar.v20.decimal_places,
        null=True,
    )
    minimo = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v20.max_digits,
        decimal_places=DigVar.v20.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var21Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v21.max_digits,
        decimal_places=DigVar.v21.decimal_places,
        null=True,
    )
    maximo = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v21.max_digits,
        decimal_places=DigVar.v21.decimal_places,
        null=True,
    )
    minimo = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v21.max_digits,
        decimal_places=DigVar.v21.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var22Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v22.max_digits,
        decimal_places=DigVar.v22.decimal_places,
        null=True,
    )
    maximo = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v22.max_digits,
        decimal_places=DigVar.v22.decimal_places,
        null=True,
    )
    minimo = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v22.max_digits,
        decimal_places=DigVar.v22.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var23Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v23.max_digits,
        decimal_places=DigVar.v23.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var24Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v24.max_digits,
        decimal_places=DigVar.v24.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


###########################


class Var101Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v101.max_digits,
        decimal_places=DigVar.v101.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "profundidad", "fecha")
        indexes = [
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var102Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v102.max_digits,
        decimal_places=DigVar.v102.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "profundidad", "fecha")
        indexes = [
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var103Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v103.max_digits,
        decimal_places=DigVar.v103.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "profundidad", "fecha")
        indexes = [
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var104Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v104.max_digits,
        decimal_places=DigVar.v104.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "profundidad", "fecha")
        indexes = [
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var105Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v105.max_digits,
        decimal_places=DigVar.v105.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "profundidad", "fecha")
        indexes = [
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var106Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v106.max_digits,
        decimal_places=DigVar.v106.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "profundidad", "fecha")
        indexes = [
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var107Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v107.max_digits,
        decimal_places=DigVar.v107.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "profundidad", "fecha")
        indexes = [
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Var108Validado(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v108.max_digits,
        decimal_places=DigVar.v108.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        default_permissions = ()
        unique_together = ("estacion_id", "profundidad", "fecha")
        indexes = [
            models.Index(fields=["usado_para_horario", "id"]),
        ]


# Create your models here.


class Viento(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=DigVar.v11.max_digits,
        decimal_places=DigVar.v11.decimal_places,
        null=True,
    )
    maximo = models.DecimalField(
        "Máximo",
        max_digits=DigVar.v11.max_digits,
        decimal_places=DigVar.v11.decimal_places,
        null=True,
    )
    minimo = models.DecimalField(
        "Mínimo",
        max_digits=DigVar.v11.max_digits,
        decimal_places=DigVar.v11.decimal_places,
        null=True,
    )
    direccion = models.DecimalField(
        "Direccion",
        max_digits=DigVar.v11.max_digits,
        decimal_places=DigVar.v11.decimal_places,
        null=True,
    )
    categoria = models.DecimalField(
        "Categoria",
        max_digits=DigVar.v11.max_digits,
        decimal_places=DigVar.v11.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]


class Agua(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    caudal = models.DecimalField(
        "Caudal",
        max_digits=DigVar.v11.max_digits,
        decimal_places=DigVar.v11.decimal_places,
        null=True,
    )
    nivel = models.DecimalField(
        "Nivel",
        max_digits=DigVar.v11.max_digits,
        decimal_places=DigVar.v11.decimal_places,
        null=True,
    )
    usado_para_horario = models.BooleanField("Usado en horario", default=False)

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
            models.Index(fields=["usado_para_horario", "id"]),
        ]
