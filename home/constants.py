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

from typing import List, NamedTuple, Optional
from pathlib import Path
import json
from functools import lru_cache


class Entry(NamedTuple):
    name: str = ""
    url_name: str = ""
    permission: str = ""


class Tab(NamedTuple):
    name: str = ""
    permission: str = ""
    item: List[Entry] = []


menu_tab_html = """
<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" id="navbarInfoRed" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
    __PESTAÑA__
    </a>
    <div class="dropdown-menu" aria-labelledby="navbarDropdown">
        __ITEMS__
    </div>
</li>
"""

menu_item_html = """<a class="dropdown-item" href="__URL__">__NOMBRE__</a>"""
menu_item_divider_html = """<div class="dropdown-divider"></div>"""


@lru_cache
def menu_struct(filename: Optional[Path] = None) -> List[Tab]:
    """Returns the menu structure.

    As the function is cached, it will be called only once when the webapp is launched.

    Args:
        filename (str): Name of the file to load

    Returns:
        List[Tab]: A list of tabs to include.
    """
    if filename is None:
        filename = Path(__file__).parent / "menu.json"

    with filename.open("r") as f:
        struct = json.load(f)

    formatted: List[Tab] = []
    for tab, details in struct.items():
        entries: List[Entry] = []
        for entry in details.get("items", []):
            entries.append(Entry(**entry))
        formatted.append(Tab(tab, details.get("permission", ""), entries))

    return formatted
