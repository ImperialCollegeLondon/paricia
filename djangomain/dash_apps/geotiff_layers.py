"""GeoTIFF layer utilities for the stations map Dash app."""

import base64
import logging
import os
from functools import lru_cache

from guardian.shortcuts import get_objects_for_user
from rasterio.warp import transform_bounds
from rio_tiler.colormap import cmap
from rio_tiler.errors import RioTilerError
from rio_tiler.io import Reader

from importing.models import MapLayerImport

_TARGET_MAPBOX_COORDS_CRS = "EPSG:4326"
"""Provides coordinates in lon/lat rather than Mercator meters."""
_TARGET_RASTER_RENDER_CRS = "EPSG:3857"
"""Provides Mercator meters for rendering raster data in Mapbox."""

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

        layer_id = f"maplayer-{layer.pk}"
        layer_index[layer_id] = {
            "id": layer_id,
            "name": str(layer.name),
            "file_path": file_path,
        }

    return layer_index


def _bounds_to_lonlat_coordinates(bounds, src_crs):
    """Transform a (left, bottom, right, top) bounds tuple into lon/lat corner
    coordinates ordered for mapbox image layers.

    Args:
        bounds: Sequence of (left, bottom, right, top) in src_crs units.
        src_crs: CRS the bounds are expressed in.

    Returns:
        list[list[float]]: Corner coordinates ordered [top-left, top-right,
            bottom-right, bottom-left].
    """
    left, bottom, right, top = bounds

    if str(src_crs) != _TARGET_MAPBOX_COORDS_CRS:
        try:
            left, bottom, right, top = transform_bounds(
                src_crs,
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


def _build_image_payload(file_path):
    """Read a georeferenced single-band GeoTIFF and render it for mapbox.

    Pixels are warped to Web Mercator (EPSG:3857) so mapbox image placement on
    a Mercator basemap stays spatially consistent. Corner coordinates are then
    transformed back to lon/lat for the mapbox API.

    Args:
        file_path: Absolute path to the GeoTIFF file on disk.

    Returns:
        dict[str, object]: Payload containing image data URI and map
            coordinates.
    """
    with Reader(input=file_path, options={}) as src:
        dataset = src.dataset
        if dataset is None:
            raise ValueError("GeoTIFF dataset could not be opened.")
        img = src.preview(
            dst_crs=_TARGET_RASTER_RENDER_CRS,
            max_size=4096,
        )
        coordinates = _bounds_to_lonlat_coordinates(
            img.bounds,
            _TARGET_RASTER_RENDER_CRS,
        )

        min_value = float(img.array.min())
        max_value = float(img.array.max())
        if max_value > min_value:
            img.rescale(in_range=((min_value, max_value),))

        png_bytes = img.render(img_format="PNG", colormap=cmap.get("viridis"))

    encoded = base64.b64encode(png_bytes).decode("ascii")
    return {
        "image": f"data:image/png;base64,{encoded}",
        "coordinates": coordinates,
    }


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
        return _build_image_payload(file_path)
    except ValueError:
        raise
    except (RioTilerError, Exception) as exc:
        raise ValueError("Layer file is not a valid georeferenced GeoTIFF.") from exc


def build_mapbox_layers(layers_raw, user):
    """Build mapbox layout layers for currently visible spatial layers.

    GeoTIFF sources are resolved server-side from currently authorised
    MapLayerImport objects and never from client store values.

    Args:
        layers_raw: Trusted spatial layer payload from server-side callback
            state.
        user: Django user used for per-object authorization.

    Returns:
        list[dict[str, object]]: Mapbox image layer dictionaries for visible
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
