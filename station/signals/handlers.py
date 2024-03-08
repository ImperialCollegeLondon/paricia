from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from station.models import (
    Basin,
    Country,
    Ecosystem,
    Institution,
    Place,
    Region,
    Station,
    StationType,
)

User = get_user_model()


@receiver(post_save, sender=Country)
@receiver(post_save, sender=Region)
@receiver(post_save, sender=Ecosystem)
@receiver(post_save, sender=Institution)
@receiver(post_save, sender=StationType)
@receiver(post_save, sender=Place)
@receiver(post_save, sender=Basin)
@receiver(post_save, sender=Station)
def set_permissions(sender, instance, **kwargs):
    """Set object-level permissions."""
    instance.set_permissions()
