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


# Create your models here.
class ConsultaGenericaFechaHoraGrafico(models.Model):
    fila = models.AutoField(primary_key=True)
    id = models.IntegerField()
    fecha = models.DateTimeField()
    valor = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    porcentaje = models.IntegerField()
    salto = models.BooleanField()

    class Meta:
        # Para que no se cree en la migracion
        # abstract = True
        managed = False


class ConsultaGenericaFechaHora(models.Model):
    fecha = models.DateTimeField(primary_key=True)
    valor = models.DecimalField(max_digits=14, decimal_places=6, null=True)

    class Meta:
        # Para que no se cree en la migracion
        managed = False


class ConsultaGenericaFecha(models.Model):
    fecha = models.DateField(primary_key=True)
    valor = models.DecimalField(max_digits=14, decimal_places=6, null=True)

    class Meta:
        # Para que no se cree en la migracion
        managed = False
