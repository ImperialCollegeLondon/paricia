from django.contrib.admin.utils import NestedObjects
from django.db import models
from django.utils.encoding import force_str
from django.utils.text import capfirst


def get_deleted_objects(
    objs: list[models.Model],
) -> tuple[list[str], dict[str, int], list[str]]:
    """Return information about related objects to be deleted.

    How to do this has been taken from https://stackoverflow.com/a/39533619/3778792

    Args:
        objs (list[models.Model]): List of objects to be deleted.

    Returns:
        tuple[list[str], dict[str, int], list[str]]: Tuple containing the following:
            - List of strings representing the objects to be deleted.
            - Dictionary containing the count of objects to be deleted for each model.
            - List of strings representing the objects that are protected from deletion
    """
    collector = NestedObjects(using="default")
    collector.collect(objs)

    def format_callback(obj):
        opts = obj._meta
        no_edit_link = f"{capfirst(opts.verbose_name)}: {force_str(obj)}"
        return no_edit_link

    to_delete = collector.nested(format_callback)
    protected = [format_callback(obj) for obj in collector.protected]
    model_count = {
        model._meta.verbose_name_plural: len(objs)
        for model, objs in collector.model_objs.items()
    }
    if len(to_delete) == 0:
        to_delete.append("None")

    return to_delete, model_count, protected
