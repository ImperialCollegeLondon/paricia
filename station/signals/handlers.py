from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from station.models import (
    Basin,
    Country,
    DeltaT,
    Ecosystem,
    Institution,
    Place,
    PlaceBasin,
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
@receiver(post_save, sender=PlaceBasin)
@receiver(post_save, sender=Station)
@receiver(post_save, sender=DeltaT)
def set_object_permissions(sender, instance, **kwargs):
    """Set object-level permissions."""
    instance.set_object_permissions()


@receiver(post_migrate)
def set_model_permissions(sender, **kwargs):
    """Set model-level permissions."""
    for model in [
        Country,
        Region,
        Ecosystem,
        Institution,
        StationType,
        Place,
        Basin,
        PlaceBasin,
        Station,
        DeltaT,
    ]:
        model.set_model_permissions()
