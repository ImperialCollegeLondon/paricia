from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from management.models import PermissionsBase

from ..models import DataImportFull, DataImportTemp

User = get_user_model()


@receiver(post_save, sender=DataImportFull)
@receiver(post_save, sender=DataImportTemp)
def set_object_permissions(sender, instance: PermissionsBase, **kwargs):
    """Set object-level permissions"."""
    instance.set_object_permissions()


@receiver(post_migrate)
def set_model_permissions(sender, **kwargs):
    """Set model-level permissions."""
    for model in [DataImportFull, DataImportTemp]:
        model.set_model_permissions()
