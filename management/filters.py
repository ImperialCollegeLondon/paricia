from django.db.models import Model
from django.db.models.query import QuerySet
from django.http import HttpRequest
from guardian.shortcuts import get_objects_for_user


class FilterVisible:
    """Filter objects the user has permission to view.

    Standard filter shows ALL objects available in the database when faced with a
    ForeignKey field. This filter shows only the objects that appear in the target model
    objects that the user has permission to view.

    If field is None, the name of the `model` model is used.

    Args:
        target (type[Model]): Model containing the objects.
        model (type[Model]): Model of the objects to display.
        field (str | None): Field to filter by. Defaults to None.
    """

    def __init__(
        self, target: type[Model], model: type[Model], field: str | None = None
    ) -> None:
        self.target = target
        self.model = model
        self.field = field or model.__name__.lower()
        self.permission = f"{target._meta.app_label}.view_{target._meta.model_name}"

    def __call__(self, request: HttpRequest | None) -> QuerySet:
        if request is None:
            return QuerySet()

        pks = (
            get_objects_for_user(request.user, self.permission, klass=self.target)
            .values_list(self.field, flat=True)
            .distinct()
        )
        return self.model.objects.filter(pk__in=pks)
