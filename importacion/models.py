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

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

from formatting.models import Format
from station.models import Station


class ImportacionBase(models.Model):
    imp_id = models.AutoField("Id", primary_key=True)
    station_id = models.ForeignKey(
        Station, models.SET_NULL, blank=True, null=True, verbose_name="Station"
    )
    for_id = models.ForeignKey(
        Format, models.SET_NULL, blank=True, null=True, verbose_name="Formato"
    )
    imp_fecha = models.DateTimeField("Fecha", auto_now_add=True)
    imp_fecha_ini = models.DateTimeField("Fecha Inicial", default=timezone.now)
    imp_fecha_fin = models.DateTimeField("Fecha Final", default=timezone.now)
    # imp_archivo = models.FileField("Archivo", upload_to='archivos/', blank=True, null=True)
    imp_observacion = models.TextField(
        "Observaciones/Anotaciones", blank=True, null=True
    )
    usuario = models.ForeignKey(
        User, models.SET_NULL, blank=True, null=True, verbose_name="Usuario"
    )

    class Meta:
        abstract = True


class Importacion(ImportacionBase):
    imp_archivo = models.FileField(
        "Archivo", upload_to="archivos/", blank=True, null=True
    )

    def get_absolute_url(self):
        return reverse("importacion:importacion_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("-imp_fecha",)
        permissions = [
            (
                "descarga_archivo_original",
                "Descargar el archivo original que fue cargado al sistema.",
            ),
        ]


class ImportacionTemp(ImportacionBase):
    imp_archivo = models.FileField("Archivo", upload_to="archivos/tmp/")

    def get_absolute_url(self):
        return reverse("importacion:importacion_temp_detail", kwargs={"pk": self.pk})

    class Meta:
        default_permissions = ()
