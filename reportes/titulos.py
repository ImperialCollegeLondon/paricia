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

from variable.models import Variable, Unidad
from estacion.models import Estacion


class Titulos():
    def titulo_grafico(self, variable):
        # returns var_nombre given var_id
        consulta = list(Variable.objects.filter(var_id=variable))

        return consulta[0]

    def titulo_unidad(self, variable):
        var=Variable.objects.get(var_id=variable)
        return var.uni_id.uni_sigla
