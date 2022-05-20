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

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from estacion.models import Estacion
from medicion.models import DigVar


# Create your models here.
class Var1Anual(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField(
        "Valor",
        max_digits=(DigVar.v1.max_digits + 2),
        decimal_places=DigVar.v1.decimal_places,
        null=True,
    )
    vacios = models.DecimalField("Vacíos %", max_digits=4, decimal_places=1)
    mes_seco = models.IntegerField(
        "mes seco",
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(12)],
        null=True,
    )
    mes_seco_valor = models.DecimalField(
        "Valor",
        max_digits=(DigVar.v1.max_digits + 2),
        decimal_places=DigVar.v1.decimal_places,
        null=True,
    )
    mes_lluvioso = models.IntegerField(
        "mes lluvioso",
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(12)],
        null=True,
    )
    mes_lluvioso_valor = models.DecimalField(
        "Valor",
        max_digits=(DigVar.v1.max_digits + 2),
        decimal_places=DigVar.v1.decimal_places,
        null=True,
    )
    dias_con_lluvia = models.IntegerField("dias con lluvia", null=True)
    dias_sin_lluvia = models.IntegerField("dias sin lluvia", null=True)
    estacionalidad = models.DecimalField(
        "estacionalidad",
        max_digits=(DigVar.v1.max_digits + 2),
        decimal_places=DigVar.v1.decimal_places,
        null=True,
    )

    class Meta:
        unique_together = ("estacion_id", "fecha")
        indexes = [
            models.Index(fields=["fecha", "estacion_id"]),
        ]
