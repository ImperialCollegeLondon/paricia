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

from django.contrib.auth.models import Group, User
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver

from home.functions import actualizar_menu_grupo, actualizar_menu_usuario


@receiver(pre_save, sender=Group)
def group_changed(sender, **kwargs):
    grupo = kwargs["instance"]
    if grupo.name == "Anonymous":
        # dont save
        pass


@receiver(m2m_changed, sender=Group.permissions.through)
def group_permissions_changed(sender, **kwargs):
    action = kwargs["action"]
    if action not in ["post_add", "post_remove", "post_clear"]:
        return None
    grupo = kwargs["instance"]
    actualizar_menu_grupo(grupo)


@receiver(m2m_changed, sender=User.user_permissions.through)
def user_permissions_changed(sender, **kwargs):
    action = kwargs["action"]
    if action not in ["post_add", "post_remove", "post_clear"]:
        return None
    usuario = kwargs["instance"]
    actualizar_menu_usuario(usuario)
