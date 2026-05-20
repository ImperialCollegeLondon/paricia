"""GeoTIFF layer utilities for the stations map Dash app."""

import base64
import logging
import os
from functools import lru_cache
from typing import Any

from guardian.shortcuts import get_objects_for_user
from rasterio.warp import transform_bounds
from rio_tiler.colormap import cmap
from rio_tiler.io import Reader

from importing.models import MapLayerImport

_TARGET_MAPBOX_COORDS_CRS = "EPSG:4326"
"""Provides coordinates in lon/lat rather than Mercator meters."""
_TARGET_RASTER_RENDER_CRS = "EPSG:3857"
"""Provides Mercator meters for rendering raster data in Mapbox."""

logger = logging.getLogger(__name__)


def available_map_layers_by_id(user: Any | None) -> dict[str, dict[str, str]]:
    """Return user-viewable GeoTIFF layers keyed by dash dropdown id.

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

    layer_index = {}
    for layer in queryset.order_by("name", "pk"):
        layer_id = f"maplayer-{layer.pk}"
        layer_index[layer_id] = {
            "id": layer_id,
            "name": str(layer.name),
            "file_path": str(layer.file.path),
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


def _build_image_payload(file_path: str) -> dict[str, Any]:
    """Read a georeferenced single-band GeoTIFF and render it for mapbox.

    Pixels are warped to Web Mercator (EPSG:3857) so mapbox image placement on
    a Mercator basemap stays spatially consistent. Corner coordinates are then
    transformed back to lon/lat for the mapbox API.

    Args:
        file_path: Absolute path to the GeoTIFF file on disk.

    Returns:
        Payload containing image data URI and map
            coordinates.
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

        band_stats = next(iter(src.statistics().values()))
        img.rescale(in_range=((band_stats.min, band_stats.max),))
        # This rescales the image pixel values to the full 0-255 range based on the min and max of the data, # noqa: E501
        # which can help improve contrast when rendering the image.

        png_bytes = img.render(img_format="PNG", colormap=cmap.get("viridis"))

    encoded = base64.b64encode(png_bytes).decode("ascii")
    return {
        "image": f"data:image/png;base64,{encoded}",
        "coordinates": coordinates,
    }


@lru_cache(maxsize=32)
def load_geotiff_payload(file_path: str, _mtime: float) -> dict[str, Any]:
    """Load and cache GeoTIFF payload from disk.

    The mtime parameter is not used directly but is part of the cache key,
    allowing the cache to invalidate when files are modified on disk.

    Args:
        file_path: Absolute path to the GeoTIFF file on disk.
        _mtime: File modification time used to invalidate cache when file
            changes.

    Returns:
        Payload containing image data URI and map
            coordinates.
    """
    return _build_image_payload(file_path)


def build_mapbox_layers(layers_raw: list, user: Any) -> list[dict[str, Any]]:
    """Build mapbox layout layers for currently visible spatial layers.

    GeoTIFF sources are resolved server-side from currently authorised
    MapLayerImport objects and never from client store values.

    Args:
        layers_raw: Trusted spatial layer payload from server-side callback
            state.
        user: Django user used for per-object authorization.

    Returns:
        Mapbox image layer dictionaries for visible
            and authorized GeoTIFF layers.
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
            mtime = os.path.getmtime(resolved_layer["file_path"])
            payload = load_geotiff_payload(resolved_layer["file_path"], mtime)
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
