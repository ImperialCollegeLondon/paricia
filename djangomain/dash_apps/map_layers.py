"""GeoTIFF layer utilities for the stations map Dash app."""

import base64
import logging
from collections.abc import Generator
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from functools import lru_cache
from typing import Any

import adlfs
import rioxarray  # noqa: F401
import xarray as xr
from azure.identity import DefaultAzureCredential
from azure.storage.blob import (
    BlobSasPermissions,
    BlobServiceClient,
    generate_blob_sas,
)
from django.core.files.storage import FileSystemStorage, default_storage
from guardian.shortcuts import get_objects_for_user
from rasterio.warp import transform_bounds
from rio_tiler.colormap import cmap
from rio_tiler.io import Reader
from rio_tiler.io.xarray import XarrayReader
from rio_tiler.models import ImageData

from importing.models import FileType, MapLayerImport

_TARGET_MAPBOX_COORDS_CRS = "EPSG:4326"
"""Provides coordinates in lon/lat rather than Mercator meters."""
_TARGET_RASTER_RENDER_CRS = "EPSG:3857"
"""Provides Mercator meters for rendering raster data in Mapbox."""

logger = logging.getLogger(__name__)


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
def _open_netcdf(file_name: str) -> Generator[xr.Dataset]:
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


def available_map_layers_by_id(user: Any | None) -> dict[str, dict[str, str | float]]:
    """Return user-viewable map layers keyed by dash dropdown id.

    Args:
        user: Django user used to resolve object-level permissions.

    Returns:
        Layer metadata keyed by maplayer id. Returns an empty dict when the
            user is None or lookup fails.
    """
    if user is None:
        return {}

    try:
        queryset = get_objects_for_user(
            user,
            "importing.view_maplayerimport",
            klass=MapLayerImport,
        )
    except Exception as e:
        logger.error("Error occurred while fetching available map layers: %s", e)
        return {}

    layer_index: dict[str, dict[str, str | float]] = {}
    for layer in queryset.order_by("name", "pk"):
        if layer.file_type == FileType.NETCDF:
            for i, timestamp in enumerate(layer.timestamps):
                layer_id = f"maplayer-{layer.pk}-{i}"
                name = f"{layer.name} ({timestamp})"
                layer_index[layer_id] = {
                    "id": layer_id,
                    "name": name,
                    "mtime": layer.updated_at.timestamp(),
                    "file_name": layer.file.name,
                    "file_type": layer.file_type,
                    "variable": layer.variable,
                    "order": i,
                }

        else:
            layer_id = f"maplayer-{layer.pk}"
            layer_index[layer_id] = {
                "id": layer_id,
                "name": str(layer.name),
                "mtime": layer.updated_at.timestamp(),
                "file_name": layer.file.name,
                "file_type": layer.file_type,
            }

    return layer_index


def _bounds_to_lonlat_coordinates(bounds: tuple, src_crs: str) -> list[list[float]]:
    """Transform a (left, bottom, right, top) bounds tuple into lon/lat corner
    coordinates ordered for mapbox image layers.

    Args:
        bounds: Sequence of (left, bottom, right, top) in src_crs units.
        src_crs: CRS the bounds are expressed in.

    Returns:
        Corner coordinates ordered [top-left, top-right,
            bottom-right, bottom-left].
    """
    left, bottom, right, top = bounds

    try:
        left, bottom, right, top = transform_bounds(
            src_crs,
            _TARGET_MAPBOX_COORDS_CRS,
            left,
            bottom,
            right,
            top,
        )
    except Exception as exc:
        raise ValueError(
            "GeoTIFF coordinates could not be transformed to lon/lat."
        ) from exc

    if not (-180 <= left <= 180 and -180 <= right <= 180):
        raise ValueError("GeoTIFF coordinates must be valid lon/lat values.")
    if not (-90 <= bottom <= 90 and -90 <= top <= 90):
        raise ValueError("GeoTIFF coordinates must be valid lon/lat values.")

    return [
        [float(left), float(top)],
        [float(right), float(top)],
        [float(right), float(bottom)],
        [float(left), float(bottom)],
    ]


def _render_image_payload(
    img: ImageData,
    coordinates: list[list],
    src: Any,
):
    """Renders a raster image and builds its Mapbox image payload.

    Args:
        img: The raster image object to render.
        coordinates: Image corner coordinates in longitude and latitude.
        src: The raster reader used to read the image data.

    Returns:
        A dictionary containing the image data URI and map coordinates.
    """
    band_stats = next(iter(src.statistics().values()))
    img.rescale(in_range=((band_stats.min, band_stats.max),))
    # This rescales the image pixel values to the full 0-255 range based on the min and max of the data, # noqa: E501
    # which can help improve contrast when rendering the image. Discussion below
    # https://github.com/developmentseed/titiler/discussions/494

    png_bytes = img.render(img_format="PNG", colormap=cmap.get("viridis"))

    encoded = base64.b64encode(png_bytes).decode("ascii")
    return {
        "image": f"data:image/png;base64,{encoded}",
        "coordinates": coordinates,
    }


def _build_netcdf_image_payload(
    file_path: str, variable: str, order: int
) -> dict[str, Any]:
    """Read data for one timestamp from a NetCDF and render it for mapbox.

    Args:
        file_path: Absolute path to the NetCDF file on disk.
        variable: Name of the variable to extract from the NetCDF file.
        order: The order of the map layer within the NetCDF file.

    Returns:
        Payload containing image data URI and map coordinates.
    """
    with _open_netcdf(file_path) as ds:
        data = ds[variable]
        timestamp_data = data.isel({"t": order})
        timestamp_data = timestamp_data.rio.set_spatial_dims(x_dim="x", y_dim="y")

        with XarrayReader(timestamp_data) as src:
            img = src.preview(
                dst_crs=_TARGET_RASTER_RENDER_CRS,
            )
            coordinates = _bounds_to_lonlat_coordinates(
                src.bounds,
                src.crs,
            )

            return _render_image_payload(img, coordinates, src)


def _build_geotiff_image_payload(file_path: str) -> dict[str, Any]:
    """Read a georeferenced single-band GeoTIFF and render it for mapbox.

    Pixels are warped to Web Mercator (EPSG:3857) so mapbox image placement on
    a Mercator basemap stays spatially consistent. Corner coordinates are then
    transformed back to lon/lat for the mapbox API.

    Args:
        file_path: Absolute path to the GeoTIFF file on disk.

    Returns:
        Payload containing image data URI and map coordinates.
    """
    with Reader(input=file_path, options={}) as src:
        dataset = src.dataset
        if dataset is None:
            raise ValueError("GeoTIFF dataset could not be opened.")
        img = src.preview(
            dst_crs=_TARGET_RASTER_RENDER_CRS,
        )
        coordinates = _bounds_to_lonlat_coordinates(
            dataset.bounds,
            src.crs,
        )

        return _render_image_payload(img, coordinates, src)


@lru_cache(maxsize=32)
def load_payload(
    file_name: str,
    _mtime: float,
    file_type: FileType,
    variable: str | None = None,
    order: int = 0,
) -> dict[str, Any]:
    """Load and cache map layer payload from disk.

    The mtime parameter is not used directly but is part of the cache key,
    allowing the cache to invalidate when files are modified on disk.

    Args:
        file_name: Name of the file to load.
        _mtime: File modification time used to invalidate cache when file
            changes.
        file_type: Whether the file is a netcdf or geotiff file.
        variable: The variable associated with the map layer if from a NetCDF.
        order: The order of the map layer within the file if from a NetCDF.

    Returns:
        Payload containing image data URI and map coordinates.

    Raises:
        ValueError: If the file type is unsupported (i.e. not a FileType.GEOTIFF or
            FileType.NETCDF).
    """
    file_path = get_map_layer_path(file_name)

    if file_type == FileType.GEOTIFF:
        return _build_geotiff_image_payload(file_path)

    if file_type == FileType.NETCDF:
        if not variable:
            raise ValueError("Variable must be specified for NetCDF files.")
        return _build_netcdf_image_payload(file_path, variable, order)

    raise ValueError(f"Unsupported file type: {file_type}")


def build_mapbox_layers(layers_raw: list, user: Any) -> list[dict[str, Any]]:
    """Build mapbox layout layers for currently visible spatial layers.

    GeoTIFF/NetCDF sources are resolved server-side from currently authorised
    MapLayerImport objects and never from client store values.

    Args:
        layers_raw: Trusted spatial layer payload from server-side callback
            state.
        user: Django user used for per-object authorization.

    Returns:
        Mapbox image layer dictionaries for visible and authorized GeoTIFF/NetCDF
            layers.
    """
    map_layers = []
    available_layers = available_map_layers_by_id(user)

    for layer in layers_raw:
        if not layer["visible"]:
            continue

        resolved_layer = available_layers.get(layer["id"])
        if not resolved_layer:
            continue

        try:
            payload = load_payload(
                resolved_layer["file_name"],
                resolved_layer["mtime"],
                resolved_layer["file_type"],
                resolved_layer.get("variable"),
                resolved_layer.get("order", 0),
            )

        except (OSError, ValueError) as exc:
            logger.warning("Skipping map layer %s: %s", layer["id"], exc)
            continue

        map_layers.append(
            {
                "type": "raster",
                "sourcetype": "image",
                "source": payload["image"],
                "coordinates": payload["coordinates"],
                "opacity": 0.75,
                "below": "traces",
            }
        )

    return map_layers
