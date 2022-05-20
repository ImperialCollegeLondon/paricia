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

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from estacion.models import Estacion
from variable.models import Variable


class CalidadPermisos(models.Model):
    class Meta:
        default_permissions = ()
        permissions = [
            ("view_graficos", "Ver gráficos VALIDADOS del módulo Calidad"),
            ("view_graficoscrudos", "Ver gráficos CRUDOS del módulo Calidad"),
            ("view_comparar_hidro", "Ver comparación datos CALIDAD vs HIDRO"),
        ]
        managed = False


class AsociacionHidro(models.Model):
    estacion_calidad = models.OneToOneField(
        Estacion, related_name="estacion_calidad", on_delete=models.SET_NULL, null=True
    )
    estaciones_hidro = models.ManyToManyField(Estacion, related_name="estaciones_hidro")

    def get_absolute_url(self):
        return reverse("calidad:asociacionhidro_index")


class UsuarioVariable(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    variable = models.ManyToManyField(Variable)

    def get_absolute_url(self):
        return reverse("calidad:usuario_variable_index")
