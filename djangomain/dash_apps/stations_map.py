"""Dash app for selecting stations and rendering them on an interactive map.

This module defines a DjangoDash application with two station checklist sections,
plus a third block for spatial layer controls. GeoTIFF layers are loaded from
MapLayerImport entries and rendered below station points.
"""

import base64
import io
import os
from functools import lru_cache
from pathlib import Path

import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import tifffile
from dash import MATCH, Input, Output, Patch, State, dcc, html, no_update
from django_plotly_dash import DjangoDash
from guardian.shortcuts import get_objects_for_user
from PIL import Image

from importing.models import MapLayerImport
from station.models import Station

SCROLL_HEIGHT = "280px"

_ALLOWED_TIFF_EXTENSIONS = {".tif", ".tiff"}
_STATION_KEYS = (
    "station_id",
    "station_code",
    "station_name",
    "station_latitude",
    "station_longitude",
)
_DEFAULT_MAP_STYLE = "carto-positron"
_MAP_STYLE_OPTIONS = [
    {"label": "Carto Positron", "value": "carto-positron"},
    {"label": "Carto Darkmatter", "value": "carto-darkmatter"},
    {"label": "OpenStreetMap", "value": "open-street-map"},
]


app = DjangoDash(
    "StationsMap",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)


def _scrollable_checklist(block_id):
    """Build a checklist wrapped in a fixed-height scroll container.

    Args:
        block_id (str): Prefix used to build the checklist component id.

    Returns:
        html.Div: Scrollable container holding a dcc.Checklist.
    """
    return html.Div(
        dcc.Checklist(
            id={"type": "checklist", "index": block_id},
            options=[],
            value=[],
            inputStyle={"marginRight": "6px"},
            labelStyle={"display": "block", "paddingBottom": "3px"},
        ),
        style={
            "maxHeight": SCROLL_HEIGHT,
            "overflowY": "auto",
            "border": "1px solid #dee2e6",
            "borderRadius": "4px",
            "padding": "6px 8px",
        },
    )


def _all_none_buttons(block_id):
    """Build the bulk-selection button group for a station checklist.

    Args:
        block_id (str): Prefix used to build the button component ids.

    Returns:
        dbc.ButtonGroup: Button group containing All and None buttons.
    """
    return dbc.ButtonGroup(
        [
            dbc.Button(
                "All",
                id={"type": "select-all", "index": block_id},
                size="sm",
                color="secondary",
                outline=True,
            ),
            dbc.Button(
                "None",
                id={"type": "select-none", "index": block_id},
                size="sm",
                color="secondary",
                outline=True,
            ),
        ],
        className="mb-2",
    )


def _station_block(block_id, title):
    """Build a station-selection card containing controls and checklist."""
    return dbc.Card(
        [
            dbc.CardHeader(title, className="py-2"),
            dbc.CardBody(
                [_all_none_buttons(block_id), _scrollable_checklist(block_id)],
                className="py-2",
            ),
        ],
        className="mb-3 shadow-sm",
    )


def _spatial_data_block():
    """Build controls for selecting and managing spatial layers."""
    return dbc.Card(
        [
            dbc.CardHeader("Spatial Data", className="py-2"),
            dbc.CardBody(
                [
                    dbc.Select(
                        id="spatial-layer-select",
                        options=[],
                        value=None,
                        size="sm",
                        className="mb-2",
                    ),
                    dbc.ButtonGroup(
                        [
                            dbc.Button(
                                "Add",
                                id="spatial-layer-add",
                                size="sm",
                                color="secondary",
                                outline=True,
                            ),
                            dbc.Button(
                                "Hide",
                                id="spatial-layer-hide",
                                size="sm",
                                color="secondary",
                                outline=True,
                            ),
                            dbc.Button(
                                "Remove",
                                id="spatial-layer-remove",
                                size="sm",
                                color="danger",
                                outline=True,
                            ),
                        ],
                        className="mb-2",
                    ),
                    html.Div(
                        id="spatial-layer-status",
                        className="small",
                        style={"minHeight": "1.25rem"},
                    ),
                ],
                className="py-2",
            ),
        ],
        className="mb-3 shadow-sm",
    )


def _map_style_block():
    """Build controls for selecting the map base style."""
    return dbc.Card(
        [
            dbc.CardHeader("Map Style", className="py-2"),
            dbc.CardBody(
                dbc.Select(
                    id="map-style-select",
                    options=_MAP_STYLE_OPTIONS,
                    value=_DEFAULT_MAP_STYLE,
                    size="sm",
                ),
                className="py-2",
            ),
        ],
        className="mb-3 shadow-sm",
    )


_sidebar = dbc.Col(
    [
        _map_style_block(),
        html.H6("Stations", className="fw-bold mb-3 mt-3 ps-1"),
        html.Div(_station_block("owned", "My Stations"), id="owned-block"),
        _station_block("public", "Public Stations"),
        _spatial_data_block(),
    ],
    width=3,
    style={
        "overflowY": "auto",
        "height": "100vh",
        "borderRight": "1px solid #dee2e6",
        "paddingRight": "12px",
    },
)

_map_col = dbc.Col(
    dcc.Graph(
        id="map_graph",
        style={"height": "50vh"},
        config={"scrollZoom": True},
        figure={
            "data": [],
            "layout": {
                "mapbox": {
                    "style": _DEFAULT_MAP_STYLE,
                    "zoom": 3.6,
                    "center": {"lat": -9.182731, "lon": -60.658738},
                },
                "margin": {"r": 0, "t": 0, "l": 0, "b": 0},
                "uirevision": True,
                "legend": {
                    "title": "",
                    "x": 0.01,
                    "y": 0.99,
                    "bgcolor": "rgba(255,255,255,0.8)",
                },
            },
        },
    ),
    width=9,
    style={"padding": "0"},
)

app.layout = dbc.Container(
    fluid=True,
    style={"height": "100vh", "padding": "0"},
    children=[
        dbc.Row([_sidebar, _map_col], className="g-0"),
        html.Div(id="stations_list", style={"display": "none"}),
        dcc.Store(
            id="spatial-layers-store",
            storage_type="memory",
            data=[],
        ),
    ],
)


# helpers


def _ensure_list(value):
    """Normalise a callback input value to a plain Python list."""
    if not value:
        return []
    return value if isinstance(value, list) else [value]


def _build_options(codes):
    """Build checklist options from station code values."""
    sorted_codes = sorted(_ensure_list(codes))
    station_names = {
        station.station_code: station.station_name
        for station in Station.objects.filter(station_code__in=sorted_codes).only(
            "station_code", "station_name"
        )
    }

    options = []
    for code in sorted_codes:
        if code not in station_names:
            continue
        name = station_names[code]
        options.append(
            {
                "label": f"{code} - {name}" if name else code,
                "value": code,
            }
        )
    return options


def _get_request_user(kwargs):
    """Get callback request user from django_plotly_dash callback kwargs."""
    request = kwargs.get("request")
    return getattr(request, "user", None)


def _layer_file_path(layer):
    """Return safe file-system path for a map layer upload."""
    try:
        return str(layer.file.path)
    except (ValueError, OSError):
        return None


def _available_map_layers_by_id(user):
    """Return user-viewable GeoTIFF layers keyed by dash dropdown id."""
    if user is None:
        return {}

    try:
        queryset = get_objects_for_user(
            user,
            "importing.view_maplayerimport",
            klass=MapLayerImport,
        )
    except Exception:
        return {}

    layer_index = {}
    for layer in queryset.order_by("name", "pk"):
        file_path = _layer_file_path(layer)
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


def _station_rows_for_codes(codes, station_group):
    """Build map rows for selected station codes in display order."""
    selected_codes = _ensure_list(codes)
    if not selected_codes:
        return []

    station_rows = {
        row["station_code"]: row
        for row in Station.objects.filter(station_code__in=selected_codes).values(
            *_STATION_KEYS
        )
    }

    rows = []
    for code in selected_codes:
        row = station_rows.get(code)
        if not row:
            continue
        rows.append({**row, "type": station_group})
    return rows


def _normalise_spatial_layers(layers_raw):
    """Normalise GeoTIFF layer data from spatial layer store."""
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


def _is_valid_lon_lat(lon, lat):
    """Return True when coordinates are plausible longitude/latitude values."""
    return -180 <= lon <= 180 and -90 <= lat <= 90


def _compute_geotiff_coordinates(width, height, pixel_scale_raw, tiepoint_raw):
    """Compute map corner coordinates from GeoTIFF model tags."""
    try:
        scale_x = float(pixel_scale_raw[0])
        scale_y = float(pixel_scale_raw[1])
        tie_i, tie_j, _, tie_lon, tie_lat, _ = [
            float(value) for value in tiepoint_raw[:6]
        ]
    except (TypeError, ValueError, IndexError) as exc:
        raise ValueError("GeoTIFF metadata contains non-numeric values.") from exc

    if scale_x == 0 or scale_y == 0:
        raise ValueError("GeoTIFF pixel scales must be non-zero.")

    left = tie_lon + (0 - tie_i) * scale_x
    right = tie_lon + (width - tie_i) * scale_x
    top = tie_lat - (0 - tie_j) * abs(scale_y)
    bottom = tie_lat - (height - tie_j) * abs(scale_y)

    if right < left:
        left, right = right, left
    if top < bottom:
        top, bottom = bottom, top

    coordinates = [
        [left, top],
        [right, top],
        [right, bottom],
        [left, bottom],
    ]
    if not all(_is_valid_lon_lat(lon, lat) for lon, lat in coordinates):
        raise ValueError("GeoTIFF coordinates must be valid lon/lat values.")

    return [[float(lon), float(lat)] for lon, lat in coordinates]


def _extract_geotiff_coordinates_from_tifffile_page(page):
    """Compute lon/lat coordinates from a tifffile page object."""
    pixel_scale_tag = page.tags.get("ModelPixelScaleTag")
    tiepoint_tag = page.tags.get("ModelTiepointTag")

    if not pixel_scale_tag or len(pixel_scale_tag.value) < 2:
        raise ValueError("GeoTIFF is missing ModelPixelScaleTag (33550).")
    if not tiepoint_tag or len(tiepoint_tag.value) < 6:
        raise ValueError("GeoTIFF is missing ModelTiepointTag (33922).")

    return _compute_geotiff_coordinates(
        page.imagewidth,
        page.imagelength,
        pixel_scale_tag.value,
        tiepoint_tag.value,
    )


def _array_to_png_data_uri(raster):
    """Convert a numeric raster array to a grayscale RGBA PNG data URI."""
    array = np.asarray(raster, dtype=float)
    if array.ndim == 3:
        array = array[..., 0]
    if array.ndim != 2:
        raise ValueError("GeoTIFF image could not be converted to a displayable PNG.")

    finite_mask = np.isfinite(array)
    if finite_mask.any():
        finite_values = array[finite_mask]
        minimum = float(finite_values.min())
        maximum = float(finite_values.max())
        if maximum > minimum:
            normalised = (np.nan_to_num(array, nan=minimum) - minimum) / (
                maximum - minimum
            )
            scaled = np.clip(normalised * 255, 0, 255).astype(np.uint8)
        else:
            scaled = np.zeros(array.shape, dtype=np.uint8)
    else:
        scaled = np.zeros(array.shape, dtype=np.uint8)

    rgba = np.zeros((*array.shape, 4), dtype=np.uint8)
    rgba[..., 0] = scaled
    rgba[..., 1] = scaled
    rgba[..., 2] = scaled
    rgba[..., 3] = np.where(finite_mask, 255, 0).astype(np.uint8)

    with io.BytesIO() as output:
        Image.fromarray(rgba, mode="RGBA").save(output, format="PNG")
        encoded = base64.b64encode(output.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


@lru_cache(maxsize=32)
def _load_geotiff_payload(file_path, mtime):
    """Load GeoTIFF and return mapbox image source plus coordinates."""
    del mtime

    tif = None
    try:
        tif = tifffile.TiffFile(file_path)
        if not tif.pages:
            raise ValueError("TIFF file has no pages.")

        page = tif.pages[0]
        coordinates = _extract_geotiff_coordinates_from_tifffile_page(page)
        image_data = _array_to_png_data_uri(page.asarray())
    except Exception as exc:
        raise ValueError("Layer file is not a valid georeferenced GeoTIFF.") from exc
    finally:
        if tif is not None:
            tif.close()

    return {"image": image_data, "coordinates": coordinates}


def _build_mapbox_layers(layers_raw, user):
    """Build mapbox layout layers for currently visible spatial layers.

    GeoTIFF sources are resolved server-side from currently authorised
    MapLayerImport objects and never from client store values.
    """
    map_layers = []
    available_layers = _available_map_layers_by_id(user)

    for layer in _normalise_spatial_layers(layers_raw):
        if not layer["visible"]:
            continue

        resolved_layer = available_layers.get(layer["id"])
        if not resolved_layer:
            continue

        try:
            mtime = os.path.getmtime(resolved_layer["file_path"])
            payload = _load_geotiff_payload(resolved_layer["file_path"], mtime)
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


# populate checklist options


@app.callback(
    [
        Output({"type": "checklist", "index": "owned"}, "options"),
        Output({"type": "checklist", "index": "public"}, "options"),
        Output("owned-block", "style"),
    ],
    Input("stations_list", "children"),
)
def populate_options(all_raw, **kwargs):
    """Populate owned and public checklist options from visible station codes."""
    all_codes = _ensure_list(all_raw)

    request = kwargs.get("request")
    user = getattr(request, "user", None)

    if user and user.is_authenticated:
        owned_codes = set(
            Station.objects.filter(station_code__in=all_codes, owner=user).values_list(
                "station_code", flat=True
            )
        )
        owned_block_style = {}
    else:
        owned_codes = set()
        owned_block_style = {"display": "none"}

    owned = [c for c in all_codes if c in owned_codes]
    public = [c for c in all_codes if c not in owned_codes]
    return _build_options(owned), _build_options(public), owned_block_style


@app.callback(
    [
        Output("spatial-layer-select", "options"),
        Output("spatial-layer-select", "value"),
    ],
    [
        Input("stations_list", "children"),
        Input("spatial-layers-store", "data"),
    ],
    State("spatial-layer-select", "value"),
)
def populate_spatial_layer_dropdown(
    _stations_raw, _layers_raw, selected_value, **kwargs
):
    """Populate spatial layer dropdown from viewable MapLayerImport objects."""
    user = _get_request_user(kwargs)
    layer_index = _available_map_layers_by_id(user)

    options = [
        {"label": layer["name"], "value": layer_id}
        for layer_id, layer in layer_index.items()
    ]

    valid_values = {option["value"] for option in options}
    if selected_value in valid_values:
        value = selected_value
    elif options:
        value = options[0]["value"]
    else:
        value = None
    return options, value


# selection


@app.callback(
    Output({"type": "checklist", "index": MATCH}, "value"),
    [
        Input({"type": "checklist", "index": MATCH}, "options"),
        Input({"type": "select-all", "index": MATCH}, "n_clicks"),
        Input({"type": "select-none", "index": MATCH}, "n_clicks"),
    ],
)
def checklist_selection(options, _n_all, _n_none, callback_context):
    triggered = (
        callback_context.triggered[0]["prop_id"] if callback_context.triggered else ""
    )
    triggered_component = triggered.rsplit(".", 1)[0]

    if "select-none" in triggered_component:
        return []

    return [o["value"] for o in (options or [])]


@app.callback(
    [
        Output("spatial-layers-store", "data"),
        Output("spatial-layer-status", "children"),
    ],
    [
        Input("spatial-layer-add", "n_clicks"),
        Input("spatial-layer-hide", "n_clicks"),
        Input("spatial-layer-remove", "n_clicks"),
    ],
    [
        State("spatial-layer-select", "value"),
        State("spatial-layers-store", "data"),
    ],
    prevent_initial_call=True,
)
def update_spatial_layers(
    _n_add,
    _n_hide,
    _n_remove,
    selected_layer_id,
    layers_raw,
    callback_context,
    **kwargs,
):
    """Apply add/hide/remove actions to spatial layer state."""
    layers = _normalise_spatial_layers(layers_raw)
    layer_by_id = {layer["id"]: dict(layer) for layer in layers}
    selected_id = selected_layer_id

    triggered = (
        callback_context.triggered[0]["prop_id"] if callback_context.triggered else ""
    )
    triggered_component = triggered.rsplit(".", 1)[0]

    user = _get_request_user(kwargs)
    available_layers = _available_map_layers_by_id(user)

    if triggered_component == "spatial-layer-add":
        if not selected_id:
            return layers, "Select a layer to add."

        selected_layer = available_layers.get(selected_id)
        if not selected_layer:
            return layers, "Selected layer is unavailable."

        try:
            mtime = os.path.getmtime(selected_layer["file_path"])
            _load_geotiff_payload(selected_layer["file_path"], mtime)
        except (OSError, ValueError) as exc:
            return layers, f"Selected layer could not be loaded: {exc}"

        if selected_id in layer_by_id:
            if layer_by_id[selected_id]["visible"]:
                return (
                    layers,
                    f'Layer "{layer_by_id[selected_id]["name"]}" is already active.',
                )

            layer_by_id[selected_id]["visible"] = True
            updated_layers = _normalise_spatial_layers(list(layer_by_id.values()))
            return (
                updated_layers,
                f'Layer "{layer_by_id[selected_id]["name"]}" is now visible.',
            )

        next_order = max((layer["order"] for layer in layers), default=0) + 1
        layers.append(
            {
                "id": selected_layer["id"],
                "name": selected_layer["name"],
                "source_kind": "geotiff",
                "visible": True,
                "order": next_order,
            }
        )
        return _normalise_spatial_layers(
            layers
        ), f'Added layer "{selected_layer["name"]}".'

    if triggered_component == "spatial-layer-hide":
        if not selected_id:
            return layers, "Select an active layer first."

        target = layer_by_id.get(selected_id)
        if not target:
            return layers, "Add the selected layer first."

        target["visible"] = not bool(target["visible"])
        updated_layers = _normalise_spatial_layers(list(layer_by_id.values()))
        visibility = "visible" if target["visible"] else "hidden"
        return updated_layers, f'Layer "{target["name"]}" is now {visibility}.'

    if triggered_component == "spatial-layer-remove":
        if not selected_id:
            return layers, "Select an active layer first."

        target = layer_by_id.get(selected_id)
        if not target:
            return layers, "Layer is not currently active."

        updated_layers = [layer for layer in layers if layer["id"] != selected_id]
        return _normalise_spatial_layers(
            updated_layers
        ), f'Removed layer "{target["name"]}".'

    return no_update, no_update


# map

_COLOR_MAP = {
    "My Stations": "#e74c3c",
    "Public": "#3498db",
}


@app.callback(
    Output("map_graph", "figure"),
    [
        Input({"type": "checklist", "index": "owned"}, "value"),
        Input({"type": "checklist", "index": "public"}, "value"),
        Input("spatial-layers-store", "data"),
        Input("map-style-select", "value"),
    ],
)
def update_map(
    owned_selected, public_selected, spatial_layers_raw, map_style_value, **kwargs
):
    """Build a scatter-mapbox figure for currently selected stations and layers."""
    rows = _station_rows_for_codes(owned_selected, "My Stations")
    rows.extend(_station_rows_for_codes(public_selected, "Public"))
    user = _get_request_user(kwargs)

    valid_styles = {option["value"] for option in _MAP_STYLE_OPTIONS}
    map_style = (
        map_style_value if map_style_value in valid_styles else _DEFAULT_MAP_STYLE
    )

    patched = Patch()
    patched["layout"]["mapbox"]["layers"] = _build_mapbox_layers(
        spatial_layers_raw,
        user,
    )

    df = pd.DataFrame(rows, columns=[*_STATION_KEYS, "type"])
    traces = []
    for group, color in _COLOR_MAP.items():
        sub = df[df["type"] == group]
        traces.append(
            go.Scattermapbox(
                lat=sub["station_latitude"],
                lon=sub["station_longitude"],
                mode="markers",
                marker={"color": color, "size": 10},
                name=group,
                hovertext=sub["station_code"],
                hoverinfo="text",
            )
        )

    patched["data"] = traces
    patched["layout"]["mapbox"]["style"] = map_style

    return patched
