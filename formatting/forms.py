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

from django.forms import ModelForm

from formatting.models import Clasification


class ClasificationForm(ModelForm):
    class Meta:
        model = Clasification
        fields = [
            "variable",
            "accumulate",
            "incremental",
            "resolution",
            "decimal_comma",
            "value",
            "value_validator_column",
            "value_validator_text",
            "maximum",
            "maximum_validator_column",
            "maximum_validator_text",
            "minimum",
            "minimum_validator_column",
            "minimum_validator_text",
        ]
