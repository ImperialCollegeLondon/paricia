import logging

import requests

from djangomain.settings import settings

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


def retrieve_thingsboard_device_id(token, customer_id, device_name):
    """Retrieve ThingsBoard device ID for a given device name."""
    api_headers = {"X-Authorization": f"Bearer {token}", "Accept": "application/json"}

    devices_url = f"https://{settings.TB_HOST}/api/customer/{customer_id}/devices?pageSize=10000&page=0"
    print(f"Using customer endpoint (customer ID: {customer_id})")

    r = requests.get(devices_url, headers=api_headers)

    if r.status_code != 200:
        raise Exception(f"Failed to retrieve devices: {r.status_code} - {r.text}")

    meta = r.json().get("data", [])

    # Filter to only the device we need
    device_ids = [x["id"]["id"] for x in meta if x.get("name") == device_name]

    if len(device_ids) == 0:
        raise Exception(f"Device '{device_name}' not found!")

    return device_ids[0]


def retrieve_thingsboard_data(
    token, customer_id, tb_device_name, variable, start_ts, end_ts
):
    """Retrieves data from ThingsBoard for a given device and variable.

    Saves the response to a JSON file in the media directory.
    """

    tb_device_id = retrieve_thingsboard_device_id(token, customer_id, tb_device_name)
    print(f"Retrieving ThingsBoard data for device {tb_device_id}, variable {variable}")
    url = (
        f"https://{settings.TB_HOST}/api/plugins/telemetry/DEVICE/{tb_device_id}/values/timeseries"
        f"?interval=60000&limit=10000&agg=NONE"
        f"&keys={variable}&startTs={start_ts}&endTs={end_ts}"
    )
    headers = {"X-Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    logger.error(f"Request URL: {url}")

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Failed to retrieve data: {response.status_code} - {response.text}"
        )
