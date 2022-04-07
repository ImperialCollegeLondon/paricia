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

from django.contrib.auth.backends import ModelBackend

from .functions import get_anonymous_user


class AnonymousPermissions(ModelBackend):
    """
    Función que permite dar permisos a usuario AnonymousUser por medio de permisos de usuario
    Solamente debe hacer override  a método has_perm de ModelBackend
    """

    def has_perm(self, user_obj, perm, obj=None):

        if not user_obj.is_anonymous:
            return user_obj.is_active and super(ModelBackend, self).has_perm(
                user_obj, perm, obj=obj
            )

        if hasattr(user_obj, "_perm_cache"):
            return perm in user_obj._perm_cache

        anon_user = get_anonymous_user()
        if not anon_user.is_active:
            return False

        perms = anon_user.get_all_permissions()
        setattr(user_obj, "_perm_cache", perms)
        return perm in user_obj._perm_cache
