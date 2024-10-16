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
from logging import getLogger

from django.contrib.auth.models import Permission, User
from django.db.models import QuerySet
from django.db.models.query import Q
from django.urls import reverse

from .frontend_menu.constants import (
    menu_item_divider_html,
    menu_item_html,
    menu_struct,
    menu_tab_html,
)


def get_menu(user: User) -> str:
    """Generate the user menu in HTML, depending on its permissions.

    Args:
        user (User): The user to generate the menu for.

    Returns:
        str: An HTML string with the menu items.
    """
    if user.is_anonymous:  # TODO check this new logic if this function is ever used
        perms = Permission.objects.filter(Q(user=user) | Q(group__in=user.groups.all()))
        is_superuser = False
    else:
        perms = Permission.objects.filter(Q(user=user) | Q(group__in=user.groups.all()))
        is_superuser = user.is_superuser

    menu = ""
    for tab in menu_struct():
        items = ""
        last_is_divider = True
        i = 0

        for elements in tab.items:
            if elements.name == "":
                if last_is_divider:
                    continue
                items += menu_item_divider_html
                last_is_divider = True
                continue

            app, codename = elements.permission.split(".")
            if (
                perms.filter(content_type__app_label=app, codename=codename).exists()
                or is_superuser
            ):
                try:
                    url = reverse(elements.url_name)
                except Exception:
                    msg = f"URL '{elements.url_name}' not found when creating menu."
                    getLogger().debug(msg)
                    continue

                items += menu_item_html.format(url=url, name=elements.name)
                last_is_divider = False
                i += 1

        if i > 0:
            menu += menu_tab_html.format(tab=tab.name, items=items)

    return menu


def modelo_a_tabla_html(modelo: QuerySet, col_extra: bool) -> str:
    """Extracts the entries in a query as an HTML table.

    NOTE: To be moved to a separates 'utilities' module.
    NOTE: There's no need to do this manually, we should use django-tables2 for
                this: https://django-tables2.readthedocs.io/en/latest/

    Args:
        modelo (QuerySet): Objects to extract as HTML
        col_extra (bool): If an extra column need to be included at the end.

    Returns:
        str: Table in HTML with the contents of a model
    """
    html_cola = "</td></tr>"
    if col_extra:
        html_cola = "</td><td></td></tr>"
    html = ""
    for row in modelo:
        html += "<tr><td>" + "</td><td>".join([str(i or "") for i in row]) + html_cola
    return html


def dictfetchall(cursor) -> list[dict]:
    """Return all rows from a cursor as a list of dict.

    TODO: This is used to process low level SQL requests, so chances are it will not be
    needed once we are done with this.
    NOTE: To be moved to a separates 'utilities' module.

    Args:
        cursor (?): ?

    Returns:
        List[Dict]: ?
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


class objdict(dict):
    """Dictionary whose content can be manipulated as attributes.

    NOTE: Might be a better option to do this. Needs deeper analysis.
    NOTE: To be moved to a separates 'utilities' module.
    """

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)
