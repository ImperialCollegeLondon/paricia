"""Utilities for reading map layer files from local or Azure Blob storage."""

from collections.abc import Generator
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta

import adlfs
import xarray as xr
from azure.identity import DefaultAzureCredential
from azure.storage.blob import (
    BlobSasPermissions,
    BlobServiceClient,
    generate_blob_sas,
)
from django.core.files.storage import FileSystemStorage, default_storage


def _generate_sas_token(file_name: str) -> str:
    """Generates a SAS token for accessing a file in Azure Blob Storage."""
    blob_service_client = BlobServiceClient(
        account_url=f"https://{default_storage.account_name}.blob.core.windows.net",
        credential=DefaultAzureCredential(),
    )
    now = datetime.now(UTC)
    start = now - timedelta(minutes=15)
    expiry = now + timedelta(hours=1)
    delegation_key = blob_service_client.get_user_delegation_key(
        key_start_time=start, key_expiry_time=expiry
    )
    sas_token = generate_blob_sas(
        account_name=default_storage.account_name,
        container_name=default_storage.azure_container,
        blob_name=file_name,
        user_delegation_key=delegation_key,
        permission=BlobSasPermissions(read=True),
        expiry=expiry,
    )
    return sas_token


def get_map_layer_path(file_name: str) -> str:
    """Get the path/URL for the map layer file.

    If stored locally (i.e. the default storage is FileSystemStorage), the local file
    path is returned. Otherwise (if stored in Azure Blob Storage), a temporary URL to
    the file is returned.

    Args:
        file_name: Name of the map layer file.

    Returns:
        The local file path or URL to the map layer file.
    """
    if isinstance(default_storage, FileSystemStorage):
        return default_storage.path(file_name)
    sas_token = _generate_sas_token(file_name)
    return (
        f"https://{default_storage.account_name}.blob.core.windows.net/"
        f"{default_storage.azure_container}/{file_name}?{sas_token}"
    )


@contextmanager
def open_netcdf(file_name: str) -> Generator[xr.Dataset]:
    """Creates a context manager to load a NetCDF dataset.

    If the file is stored locally, it is opened directly. If stored in Azure Blob
    Storage, 'adlfs' is used to access the file using a temporary SAS token. adlfs
    is needed as the NetCDF engine cannot read directly from the Azure URL (as it
    interprets URLs as OpeNDAP endpoints).

    Args:
        file_name: Name of the NetCDF file to open.

    Yields:
        An xarray.Dataset object representing the NetCDF data.
    """
    if isinstance(default_storage, FileSystemStorage):
        with xr.open_dataset(
            default_storage.path(file_name),
            engine="netcdf4",
            decode_coords="all",
        ) as ds:
            yield ds
        return

    fs = adlfs.AzureBlobFileSystem(
        account_name=default_storage.account_name,
        sas_token=_generate_sas_token(file_name),
    )
    blob_path = f"{default_storage.azure_container}/{file_name}"

    with fs.open(blob_path, mode="rb") as file_obj:
        with xr.open_dataset(file_obj, engine="netcdf4", decode_coords="all") as ds:
            yield ds
