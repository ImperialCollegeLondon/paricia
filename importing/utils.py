import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def create_default_origins(apps, schema_editor):
    """Creates the default origins for data import."""
    ImportOrigin = apps.get_model("importing", "ImportOrigin")

    origins = ["file", "api", "Thingsboard"]
    for origin in origins:
        ImportOrigin.objects.create(origin=origin)


def remove_default_origins(apps, schema_editor):
    """Removes the default origins for data import."""
    ImportOrigin = apps.get_model("importing", "ImportOrigin")

    origins = ["file", "api", "Thingsboard"]
    for origin in origins:
        ImportOrigin.objects.filter(origin=origin).delete()


def retrieve_thingsboard_device_id(
    token: str, customer_id: str, device_name: str
) -> str:
    """Retrieve ThingsBoard device ID for a given device name."""
    api_headers = {"X-Authorization": f"Bearer {token}", "Accept": "application/json"}

    assert settings.TB_CUSTOMER_DEVICES_URL is not None
    devices_url = settings.TB_CUSTOMER_DEVICES_URL.format(customer_id=customer_id)
    logger.debug(f"Using customer endpoint (customer ID: {customer_id})")

    r = requests.get(devices_url, headers=api_headers)

    if r.status_code != 200:
        raise Exception(f"Failed to retrieve devices: {r.status_code} - {r.text}")

    meta = r.json().get("data", [])

    # Filter to only the device we need
    device_ids = [x["id"]["id"] for x in meta if x.get("name") == device_name]

    if len(device_ids) == 0:
        raise Exception(f"Device '{device_name}' not found!")

    if len(device_ids) > 1:
        logger.warning(
            "Expected one ThingsBoard device named '%s', found %d. Using first match.",
            device_name,
            len(device_ids),
        )

    return device_ids[0]


def retrieve_thingsboard_data(
    token: str,
    customer_id: str,
    tb_device_name: str,
    variable: str,
    start_ts: int,
    end_ts: int,
) -> dict:
    """Retrieves data from ThingsBoard for a given device and variable.

    Saves the response to a JSON file in the media directory.
    """

    tb_device_id = retrieve_thingsboard_device_id(token, customer_id, tb_device_name)
    logger.debug(
        f"Retrieving ThingsBoard data for device {tb_device_id}, variable {variable}"
    )
    assert settings.TB_TIMESERIES_URL is not None
    url = settings.TB_TIMESERIES_URL.format(tb_device_id=tb_device_id)
    headers = {"X-Authorization": f"Bearer {token}"}
    params: dict[str, str | int] = {
        "interval": 60000,
        "limit": 10000,
        "agg": "NONE",
        "keys": variable,
        "startTs": start_ts,
        "endTs": end_ts,
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Failed to retrieve data: {response.status_code} - {response.text}"
        )
