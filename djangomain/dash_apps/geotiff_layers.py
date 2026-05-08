"""GeoTIFF layer utilities for the stations map Dash app."""

import base64
import io
import logging
import os
from functools import lru_cache
from pathlib import Path

import numpy as np
import rasterio
from guardian.shortcuts import get_objects_for_user
from matplotlib import cm
from matplotlib.colors import Normalize
from PIL import Image
from rasterio.enums import Resampling
from rasterio.vrt import WarpedVRT
from rasterio.warp import transform_bounds

from importing.models import MapLayerImport

_ALLOWED_TIFF_EXTENSIONS = {".tif", ".tiff"}
_TARGET_MAPBOX_COORDS_CRS = "EPSG:4326"
_TARGET_RASTER_RENDER_CRS = "EPSG:3857"

logger = logging.getLogger(__name__)


def available_map_layers_by_id(user):
    """Return user-viewable GeoTIFF layers keyed by dash dropdown id.

    Args:
        user: Django user used to resolve object-level permissions.

    Returns:
        dict[str, dict[str, str]]: Layer metadata keyed by maplayer id. Returns
            an empty dict when the user is None or lookup fails.
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

    layer_index = {}
    for layer in queryset.order_by("name", "pk"):
        try:
            file_path = str(layer.file.path)
        except (ValueError, OSError):
            continue

        if (
            not file_path
            or Path(file_path).suffix.lower() not in _ALLOWED_TIFF_EXTENSIONS
        ):
            continue

        layer_id = f"maplayer-{layer.pk}"
        layer_index[layer_id] = {
            "id": layer_id,
            "name": str(layer.name),
            "file_path": file_path,
        }

    return layer_index


def normalise_spatial_layers(layers_raw):
    """Normalise GeoTIFF layer data from spatial layer store.

    Args:
        layers_raw: Raw list-like layer payload from the client store.

    Returns:
        list[dict[str, object]]: De-duplicated and sorted GeoTIFF layer
            dictionaries containing id, name, source_kind, visible and order.
    """
    layers = []
    seen_ids = set()

    for index, raw in enumerate(layers_raw if isinstance(layers_raw, list) else []):
        if not isinstance(raw, dict):
            continue

        layer_id = str(raw.get("id", "")).strip()
        if not layer_id or layer_id in seen_ids:
            continue
        seen_ids.add(layer_id)

        source_kind = str(raw.get("source_kind", "")).strip().lower()
        if source_kind != "geotiff":
            continue

        order = raw.get("order", index + 1)
        if not isinstance(order, int | float):
            order = index + 1

        layers.append(
            {
                "id": layer_id,
                "name": str(raw.get("name", "")).strip() or f"Layer {index + 1}",
                "source_kind": "geotiff",
                "visible": bool(raw.get("visible", True)),
                "order": int(order),
            }
        )

    return sorted(layers, key=lambda layer: layer["order"])


def _extract_geotiff_coordinates_from_dataset(dataset, transform_bounds_fn):
    """Compute lon/lat coordinates from a rasterio dataset.

    Args:
        dataset: Open rasterio dataset with bounds and optional CRS metadata.
        transform_bounds_fn: Callable used to transform dataset bounds to
            EPSG:4326.

    Returns:
        list[list[float]]: Image corner coordinates ordered for mapbox image
            layers as [top-left, top-right, bottom-right, bottom-left].
    """
    if not dataset.crs and dataset.transform.is_identity:
        raise ValueError("GeoTIFF is missing georeferencing metadata.")

    left, bottom, right, top = dataset.bounds

    if dataset.crs:
        try:
            left, bottom, right, top = transform_bounds_fn(
                dataset.crs,
                _TARGET_MAPBOX_COORDS_CRS,
                left,
                bottom,
                right,
                top,
                densify_pts=21,
            )
        except Exception as exc:
            raise ValueError(
                "GeoTIFF coordinates could not be transformed to lon/lat."
            ) from exc

    coordinates = [
        [left, top],
        [right, top],
        [right, bottom],
        [left, bottom],
    ]
    if not all(-180 <= lon <= 180 and -90 <= lat <= 90 for lon, lat in coordinates):
        raise ValueError("GeoTIFF coordinates must be valid lon/lat values.")

    return [[float(lon), float(lat)] for lon, lat in coordinates]


def _scale_to_uint8(values, finite_mask):
    """Scale array values to an 8-bit range using finite values only.

    Args:
        values: Numeric array to scale.
        finite_mask: Boolean mask indicating finite values.

    Returns:
        np.ndarray: uint8 array scaled into the range [0, 255].
    """
    if not finite_mask.any():
        return np.zeros(values.shape, dtype=np.uint8)

    finite_values = values[finite_mask]
    minimum = float(finite_values.min())
    maximum = float(finite_values.max())
    if maximum <= minimum:
        return np.zeros(values.shape, dtype=np.uint8)

    norm = (np.nan_to_num(values, nan=minimum) - minimum) / (maximum - minimum)
    return np.clip(norm * 255, 0, 255).astype(np.uint8)


def _apply_viridis_like(norm):
    """Map normalised [0,1] values to RGB using matplotlib viridis.

    Args:
        norm: Array-like normalised values expected in [0.0, 1.0].

    Returns:
        np.ndarray: RGB uint8 array with shape (..., 3).
    """
    rgba = np.asarray(
        cm.get_cmap("viridis")(np.clip(norm, 0.0, 1.0), bytes=True),
        dtype=np.uint8,
    )
    return rgba[..., :3]


def _array_to_png_data_uri(raster):
    """Convert a numeric raster array to a color RGBA PNG data URI.

    Args:
        raster: 2D single-band or 3D multi-band raster data.

    Returns:
        str: Base64 encoded PNG as a data URI.
    """
    array = np.asarray(raster, dtype=float)

    # Handle channel-first arrays: (C, H, W) -> (H, W, C)
    if array.ndim == 3 and array.shape[0] in (3, 4) and array.shape[-1] not in (3, 4):
        array = np.moveaxis(array, 0, -1)

    if array.ndim == 3 and array.shape[-1] >= 3:
        # True-color TIFF: keep RGB information
        rgb_source = array[..., :3]
        finite_mask = np.isfinite(rgb_source).all(axis=-1)
        rgb = np.zeros(rgb_source.shape, dtype=np.uint8)
        for ch in range(3):
            rgb[..., ch] = _scale_to_uint8(rgb_source[..., ch], finite_mask)
    elif array.ndim == 2:
        # Single-band TIFF: pseudocolor it
        finite_mask = np.isfinite(array)
        if finite_mask.any():
            finite_values = array[finite_mask]
            minimum = float(finite_values.min())
            maximum = float(finite_values.max())

            if maximum > minimum:
                normaliser = Normalize(vmin=minimum, vmax=maximum, clip=True)
                normalised = normaliser(np.nan_to_num(array, nan=minimum))
                rgb = _apply_viridis_like(normalised)
            else:
                rgb = np.zeros((*array.shape, 3), dtype=np.uint8)
        else:
            rgb = np.zeros((*array.shape, 3), dtype=np.uint8)
    else:
        raise ValueError("GeoTIFF image could not be converted to a displayable PNG.")

    alpha = np.where(finite_mask, 255, 0).astype(np.uint8)
    rgba = np.dstack((rgb, alpha))

    with io.BytesIO() as output:
        Image.fromarray(rgba, mode="RGBA").save(output, format="PNG")
        encoded = base64.b64encode(output.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def _build_image_payload_from_dataset(dataset):
    """Build image payload from an open raster dataset.

    Args:
        dataset: Open rasterio dataset or WarpedVRT dataset.

    Returns:
        dict[str, object]: Payload containing image data URI and map
            coordinates.
    """
    coordinates = _extract_geotiff_coordinates_from_dataset(
        dataset,
        transform_bounds,
    )

    raster = dataset.read(masked=True)
    if dataset.count == 1:
        raster = raster[0]
    elif dataset.count > 4:
        raster = raster[:3]

    image_data = _array_to_png_data_uri(raster.filled(np.nan))
    return {"image": image_data, "coordinates": coordinates}


@lru_cache(maxsize=32)
def load_geotiff_payload(file_path, mtime):
    """Load GeoTIFF and return mapbox image source plus coordinates.

    Args:
        file_path: Absolute path to the GeoTIFF file on disk.
        mtime: File modification time used as part of the cache key.

    Returns:
        dict[str, object]: Payload containing image data URI and map
            coordinates.
    """
    del mtime

    try:
        with rasterio.open(file_path) as dataset:
            if dataset.count < 1:
                raise ValueError("TIFF file has no bands.")

            # For CRS-aware rasters, always render from a Web Mercator VRT.
            if dataset.crs:
                with WarpedVRT(
                    dataset,
                    crs=_TARGET_RASTER_RENDER_CRS,
                    resampling=Resampling.bilinear,
                ) as warped_dataset:
                    return _build_image_payload_from_dataset(warped_dataset)

            # Fall back to the source raster only when CRS metadata is absent.
            return _build_image_payload_from_dataset(dataset)
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError("Layer file is not a valid georeferenced GeoTIFF.") from exc


def build_mapbox_layers(layers_raw, user):
    """Build mapbox layout layers for currently visible spatial layers.

    GeoTIFF sources are resolved server-side from currently authorised
    MapLayerImport objects and never from client store values.

    Args:
        layers_raw: Raw spatial layer payload from the client state.
        user: Django user used for per-object authorization.

    Returns:
        list[dict[str, object]]: Mapbox image layer dictionaries for visible
            and authorized GeoTIFF layers.
    """
    map_layers = []
    available_layers = available_map_layers_by_id(user)

    for layer in normalise_spatial_layers(layers_raw):
        if not layer["visible"]:
            continue

        resolved_layer = available_layers.get(layer["id"])
        if not resolved_layer:
            continue

        try:
            mtime = os.path.getmtime(resolved_layer["file_path"])
            payload = load_geotiff_payload(resolved_layer["file_path"], mtime)
        except (OSError, ValueError):
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
