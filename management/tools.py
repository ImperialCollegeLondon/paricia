import json
import os

import requests
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


def thingsboard_token_generator(tb_username: str, tb_password: str):
    """Generate a token for Thingsboard API authentication."""

    ip = os.getenv("TB_HOST")
    login_url = f"https://{ip}/api/auth/login"
    login_payload = json.dumps({"username": tb_username, "password": tb_password})
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    response = requests.post(login_url, headers=headers, data=login_payload)

    if response.status_code == 200:
        token = response.json().get("token")
        return token
    else:
        raise Exception(f"Failed to authenticate with Thingsboard API: {response.text}")


def retrieve_thingsboard_customerid(token: str):
    """Retrieve the customer ID for the authenticated user."""
    ip = os.getenv("TB_HOST")
    url = f"https://{ip}/api/auth/user"
    headers = {"X-Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        customer_id = user_info.get("customerId", {}).get("id")
        return customer_id
    else:
        raise Exception(
            f"Failed to retrieve user info: {response.status_code} - {response.text}"
        )
