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

from django.db import models


class PermissionsHome(models.Model):
    """Model used to define the permission "carga_inicial".

    This permission is use to show the interface to fill tables using default data. It
    doesn't create a model in the database.
    """

    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ("carga_inicial", "Carga de datos ejemplo: formatos, marcas datalogger."),
        )
