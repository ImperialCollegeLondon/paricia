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

from django.http import HttpRequest

from ..functions import get_menu


def menu(request: HttpRequest) -> dict[str, str]:
    """Context processor for creating the menus.

    Using this processor is indicated in the TEMPLATES section of settings.py.

    Args:
        request (HttpRequest): The request to process, including the 'user'.

    Returns:
        Dict[str, str]: A dictionary with the menu items.
    """
    return {"menu": get_menu(request.user)}
