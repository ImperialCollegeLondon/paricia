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

from django.forms import ModelForm
from formato.models import Clasificacion

class ClasificacionForm(ModelForm):
    class Meta:
        model = Clasificacion
        fields = ['var_id', 'coma_decimal', 'cla_valor', 'cla_maximo', 'cla_minimo',
                  'acumular', 'incremental', 'resolucion',
                  'col_validador_valor', 'txt_validador_valor',
                  'col_validador_maximo', 'txt_validador_maximo',
                  'col_validador_minimo', 'txt_validador_minimo'
                  ]

