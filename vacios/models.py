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

class VaciosPermisos(models.Model):
    class Meta:
        default_permissions = ()
        permissions = [
            ("view_vacios", "Ver vacíos de información"),
        ]
        managed = False


class consulta(models.Model):
    tipo = models.CharField(max_length=5)
    fecha_inicio = models.DateTimeField(primary_key=True)
    fecha_fin = models.DateTimeField()
    intervalo_horas = models.DecimalField(max_digits=7, decimal_places=1)

    class Meta:
        managed = False
        permissions = ()