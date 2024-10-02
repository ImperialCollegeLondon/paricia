from django.contrib.admin.utils import NestedObjects
from django.db import models
from django.utils.encoding import force_str
from django.utils.text import capfirst


def get_deleted_objects(
    objs: list[models.Model],
) -> tuple[list[str], dict[str, int], list[str]]:
    """Return information about related objects to be deleted."""
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
    return to_delete, model_count, protected
