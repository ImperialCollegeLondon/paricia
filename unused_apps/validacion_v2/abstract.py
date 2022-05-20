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

from django.db import models


class ReporteDiarioPrecipitacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateField()
    fecha_error = models.IntegerField()
    valor = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    porcentaje = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    porcentaje_error = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    valor_numero = models.IntegerField()
    valor_error = models.BooleanField
    media_historica = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    estado = models.BooleanField()
    validado = models.BooleanField()

    class Meta:
        managed = False


class ReporteDiario(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateTimeField()
    fecha_error = models.IntegerField()
    valor = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    n_valor = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    maximo = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    minimo = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    porcentaje = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    porcentaje_error = models.BooleanField()
    valor_error = models.BooleanField()
    maximo_error = models.BooleanField()
    minimo_error = models.BooleanField()
    valor_numero = models.IntegerField()
    maximo_numero = models.IntegerField()
    minimo_numero = models.IntegerField()
    estado = models.BooleanField()

    class Meta:
        ### Para que no se cree en la migracion
        managed = False


class ReporteCrudos(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateTimeField()
    valor = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    estado = models.BooleanField()
    seleccionado = models.BooleanField()
    comentario = models.CharField(max_length=250)

    class Meta:
        ### Para que no se cree en la migracion
        managed = False
