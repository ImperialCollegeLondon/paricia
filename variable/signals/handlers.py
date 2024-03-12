from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from variable.models import SensorInstallation, Unit, Variable

User = get_user_model()


@receiver(post_save, sender=SensorInstallation)
@receiver(post_save, sender=Unit)
@receiver(post_save, sender=Variable)
def set_permissions(sender, instance, **kwargs):
    """Set object-level permissions"."""
    instance.set_permissions()
