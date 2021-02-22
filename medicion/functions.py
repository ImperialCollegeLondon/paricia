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


class ReporteValidacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    estado = models.BooleanField()
    fecha = models.DateTimeField()
    valor_seleccionado = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    valor = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    variacion_consecutiva = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    comentario = models.CharField(max_length=350)
    class_fila = models.CharField(max_length=30)
    class_fecha = models.CharField(max_length=30)
    class_validacion = models.CharField(max_length=30)
    class_valor = models.CharField(max_length=30)
    class_variacion_consecutiva = models.CharField(max_length=30)
    class_stddev_error = models.CharField(max_length=30)
    class Meta:
        managed = False ### Para que no se cree en la migracion

    class Meta:
        ### Para que no se cree en la migracion
        managed = False
