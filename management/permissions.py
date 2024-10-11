"""Customised permissions."""

from django.db import models as model
from guardian.shortcuts import get_objects_for_user
from rest_framework.permissions import DjangoModelPermissions


class CustomDjangoModelPermissions(DjangoModelPermissions):
    """Modify DjangoModelPermissions to allow only users with view permissions to do
    GET, OPTIONS and HEAD requests.
    """

    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": ["%(app_label)s.view_%(model_name)s"],
        "HEAD": ["%(app_label)s.view_%(model_name)s"],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }


def get_queryset(db_field: model.Field, user: model.Model) -> model.QuerySet:
    """Return a queryset based on the permissions of the user.

    Returns queryset of public objects and objects that the user has change permisions
    for. For the case of `Station` objects, having the `change` permission is
    necessary to include the object in the queryset - being `Public` is not enough.

    Args:
        db_field (model.Field): Field to filter.
        user (model.Model): User to check permissions for.

    Returns:
        model.QuerySet: Queryset of objects that the user has permissions for.
    """
    app_name = db_field.related_model._meta.app_label
    model_name = db_field.related_model._meta.model_name
    user_objects = get_objects_for_user(user, f"{app_name}.change_{model_name}")
    public_objects = (
        db_field.related_model.objects.none()
        if model_name == "station"
        else db_field.related_model.objects.filter(visibility="public")
    )
    return user_objects | public_objects
