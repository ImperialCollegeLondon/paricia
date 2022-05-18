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

import re

from django.contrib.auth.models import AnonymousUser, Group, Permission, User
from django.db.models import Q
from django.urls import reverse

from .constants import (
    menu_item_divider_html,
    menu_item_html,
    menu_struct,
    menu_tab_html,
)

menu = {}


def get_anonymous_user():
    try:
        anon_user = User.objects.get(username="AnonymousUser")
    except:
        anon_user = User.objects.create_user(
            username="AnonymousUser",
            is_active=True,
            is_superuser=False,
            is_staff=False,
        )
    return anon_user


def generar_menu_usuario(usuario):
    if usuario.id is None:
        usuario = get_anonymous_user()
        perms = Permission.objects.filter(
            Q(user=usuario) | Q(group__in=usuario.groups.all())
        )
        is_superuser = False
    else:
        perms = Permission.objects.filter(
            Q(user=usuario) | Q(group__in=usuario.groups.all())
        )
        is_superuser = usuario.is_superuser

    _menu = ""
    for tab in menu_struct:
        items = ""
        ultimo_es_divisor = True
        i = 0
        for e in tab["items"]:
            if e["nombre"] == "":
                if ultimo_es_divisor:
                    continue
                items += menu_item_divider_html
                ultimo_es_divisor = True
                continue

            app, codename = e["permiso"].split(".")
            if (
                perms.filter(content_type__app_label=app, codename=codename).exists()
                or is_superuser
            ):
                try:
                    url = reverse(e["url_name"])
                except:
                    continue

                if not is_superuser:
                    # tab_name = re.sub("<small>.*</small>", "", e['nombre'])
                    tab_name = e["nombre"]
                else:
                    tab_name = e["nombre"]
                items += menu_item_html.replace("__URL__", url).replace(
                    "__NOMBRE__", tab_name
                )
                ultimo_es_divisor = False
                i += 1
        if i > 0:
            _menu += menu_tab_html.replace("__PESTAÑA__", tab["pestaña"]).replace(
                "__ITEMS__", items
            )
    return _menu


def actualizar_menu_usuario(usuario):
    menu[usuario.id] = generar_menu_usuario(usuario)


def actualizar_menu_grupo(grupo):
    users = User.objects.filter(groups=grupo)
    for user in users:
        menu[user.id] = generar_menu_usuario(user)


def get_menu(usuario):
    user_id = usuario.id
    if user_id is None:
        usuario = get_anonymous_user()
        user_id = usuario.id

    if not user_id in menu:
        menu[user_id] = generar_menu_usuario(usuario)
    return menu[user_id]


def modelo_a_select_html(modelo, col_extra):
    html_cola = "</td></tr>"
    if col_extra:
        html_cola = "</td><td></td></tr>"
    html = ""
    for row in modelo:
        html += "<tr><td>" + "</td><td>".join([str(i or "") for i in row]) + html_cola
    return html


def modelo_a_tabla_html(modelo, col_extra):
    html_cola = "</td></tr>"
    if col_extra:
        html_cola = "</td><td></td></tr>"
    html = ""
    for row in modelo:
        html += "<tr><td>" + "</td><td>".join([str(i or "") for i in row]) + html_cola
    return html


def modelo_a_js(modelo):
    js = "["
    for row in modelo:
        js += "['" + "','".join([str(i or "") for i in row]) + "'],"
    js += "]"
    return js


def dictfetchall(cursor):
    # Return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


class objdict(dict):
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
