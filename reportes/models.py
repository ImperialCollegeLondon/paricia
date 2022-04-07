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


class ReportesPermisos(models.Model):
    class Meta:
        default_permissions = ()
        permissions = [
            ("view_anuario", "Ver Anuario"),
            ("view_comparacionvalores", "Ver Comparación de valores"),
            ("view_comparacionvariables", "Ver Comparación de variables"),
            ("view_consultasperiodo", "Ver Consultas por períodos"),
            (
                "view_calidadconsultasperiodo",
                "Ver Consultas por períodos módulo de Calidad",
            ),
            ("reportes_general", "Reportes general esencial"),
            ("view_diario", "Ver Diario"),
            ("view_mensualmultianual", "Ver Mensual Multianual"),
            ("view_manual", "Ver manual"),
        ]
        managed = False


# Para usar en: Mediciones(crudos) y validados
class ConsultaGenericaFechaHora(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha = models.DateTimeField()
    valor = models.DecimalField(max_digits=14, decimal_places=6, null=True)

    class Meta:
        ### Para que no se cree en la migracion
        managed = False
        default_permissions = ()


# Para usar en: Mediciones(crudos) y validados. Con el indicador de saltos temporales
# Salto temporal se define cuando entre dato y dato pasa más tiempo del esperado
class ConsultaGenericaFechaHora_Saltos(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha = models.DateTimeField()
    valor = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    salto = models.BooleanField()

    class Meta:
        ### Para que no se cree en la migracion
        managed = False
        default_permissions = ()


# Para consulta datos: Horarios
class ConsultaReporteFechaHora(models.Model):
    fecha = models.DateTimeField(primary_key=True)
    valor = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    vacios = models.DecimalField(max_digits=4, decimal_places=1, null=True)

    class Meta:
        ### Para que no se cree en la migracion
        managed = False
        default_permissions = ()


# Para consulta datos: Diarios, Mensuales
class ConsultaReporteFecha(models.Model):
    fecha = models.DateField(primary_key=True)
    valor = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    vacios = models.DecimalField(max_digits=4, decimal_places=1, null=True)

    class Meta:
        ### Para que no se cree en la migracion
        managed = False
        default_permissions = ()
