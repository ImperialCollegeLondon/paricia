from contextlib import suppress

from django.db.models import ForeignKey, Model


def model_to_dict(instance: Model) -> dict:
    """Convert a model instance to a dictionary.

    For ForeignKey fields, the related model instance is converted to a string, so that
    a meaningful representation is shown in the dictionary instead of the primary key.

    Args:
        instance (Model): Model instance to convert.

    Returns:
        dict: Dictionary with the model instance data.
    """
    data = {}
    for field in instance._meta.get_fields():
        data[field.name] = field.value_from_object(instance)
        if isinstance(field, ForeignKey):
            with suppress(field.related_model.DoesNotExist):
                data[field.name] = str(
                    field.related_model.objects.get(pk=data[field.name])
                )
    return data
