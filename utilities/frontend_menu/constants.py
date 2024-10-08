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

import json
from functools import lru_cache
from pathlib import Path
from typing import NamedTuple


class Entry(NamedTuple):
    name: str = ""
    url_name: str = ""
    permission: str = ""


class Tab(NamedTuple):
    name: str = ""
    permission: str = ""
    items: list[Entry] = []


menu_tab_html = """
<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" id="navbarInfoRed" role="button"
    data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
    {tab}
    </a>
    <div class="dropdown-menu" aria-labelledby="navbarDropdown">
        {items}
    </div>
</li>
"""

menu_item_html = """<a class="dropdown-item" href="{url}">{name}</a>"""
menu_item_divider_html = """<div class="dropdown-divider"></div>"""


@lru_cache
def menu_struct(filename: Path | None = None) -> list[Tab]:
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

    formatted: list[Tab] = []
    for tab, details in struct.items():
        entries: list[Entry] = []
        for entry in details.get("items", []):
            entries.append(Entry(**entry))
        formatted.append(Tab(tab, details.get("permission", ""), entries))

    return formatted
