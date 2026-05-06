"""Dash app for selecting stations and rendering them on an interactive map.

This module defines a DjangoDash application with two station checklist sections,
plus a third block for spatial layer controls. GeoTIFF layers are loaded from
MapLayerImport entries and rendered below station points.
"""

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from dash import MATCH, Input, Output, Patch, State, dcc, html, no_update
from django_plotly_dash import DjangoDash

from djangomain.dash_apps.geotiff_layers import (
    available_map_layers_by_id,
    build_mapbox_layers,
)
from station.models import Station

SCROLL_HEIGHT = "280px"

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
        html.Div: Scrollable container holding a ``dcc.Checklist``.
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
        dbc.ButtonGroup: Button group containing *All* and *None* buttons.
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
    """Build a station-selection card containing bulk controls and a checklist.

    Args:
        block_id (str): Prefix used for internal control ids.
        title (str): Text rendered in the card header.

    Returns:
        dbc.Card: Card containing an All/None button group and a scrollable
            checklist.
    """
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
    """Build controls for selecting and toggling spatial layers.

    Returns:
        dbc.Card: Card containing a checklist of available spatial layers.
    """
    return dbc.Card(
        [
            dbc.CardHeader("Spatial Data", className="py-2"),
            dbc.CardBody(
                html.Div(
                    dcc.Checklist(
                        id="spatial-layer-checklist",
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
                ),
                className="py-2",
            ),
        ],
        className="mb-3 shadow-sm",
    )


def _map_style_block():
    """Build controls for selecting the map base style.

    Returns:
        dbc.Card: Card containing the base map style selector.
    """
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
    style={"height": "100vh", "padding": "0.5"},
    children=[
        dbc.Row([_sidebar, _map_col], className="g-0"),
        html.Div(id="stations_list", style={"display": "none"}),
    ],
)


# ── helpers ───────────────────────────────────────────────────────────────────


def _ensure_list(value):
    """Normalise a callback input value to a plain Python list.

    Args:
        value: Input that may be ``None``, a scalar, or a list.

    Returns:
        list: Empty list for falsy input; the original list; or a single-item
            list wrapping a scalar value.
    """
    if not value:
        return []
    return value if isinstance(value, list) else [value]


def _build_options(codes):
    """Build Dash checklist option dicts from an iterable of station codes.

    Each option label is ``"<code> - <name>"`` when the station has a name,
    otherwise just the code. Codes are sorted alphabetically.

    Args:
        codes (Iterable[str]): Station codes to include.

    Returns:
        list[dict[str, str]]: Option dicts with ``"label"`` and ``"value"``
            keys, ready for use in ``dcc.Checklist``.
    """
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
    """Get callback request user from django_plotly_dash callback kwargs.

    Args:
        kwargs (dict): Callback keyword arguments from django_plotly_dash.

    Returns:
        object | None: Authenticated user object when present, else None.
    """
    request = kwargs.get("request")
    return getattr(request, "user", None)


def _station_rows_for_codes(codes, station_group):
    """Build map rows for selected station codes in display order.

    Args:
        codes: Selected station codes in desired output order.
        station_group (str): Label used to tag rows for trace grouping.

    Returns:
        list[dict[str, object]]: Station row dictionaries ready for map
            trace construction.
    """
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
    """Populate owned and public checklist options from visible station codes.

    For authenticated users the owned section is shown and populated with
    stations that belong to the current user; the remaining visible stations
    go into the public section.  For anonymous users all visible stations are
    treated as public and the owned section is hidden.

    Args:
        all_raw (list[str] | str | None): Raw children value of the hidden
            ``stations_list`` div, containing the station codes the current
            user may see.
        **kwargs: Extra keyword arguments injected by ``django_plotly_dash``,
            expected to include ``request``.

    Returns:
        tuple[list[dict], list[dict], dict]: Owned checklist options, public
            checklist options, and a CSS style dict for the owned block.
    """
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
        Output("spatial-layer-checklist", "options"),
        Output("spatial-layer-checklist", "value"),
    ],
    Input("stations_list", "children"),
    State("spatial-layer-checklist", "value"),
)
def populate_spatial_layer_checklist(_stations_raw, selected_values, **kwargs):
    """Populate spatial layer checklist from viewable MapLayerImport objects.

    Args:
        _stations_raw: Unused trigger input for station list changes.
        selected_values: Currently checked layer ids.
        **kwargs: Callback kwargs containing request context.

    Returns:
        tuple[list[dict[str, str]], list[str]]: Checklist options and checked
            values.
    """
    user = _get_request_user(kwargs)
    layer_index = available_map_layers_by_id(user)

    options = [
        {"label": layer["name"], "value": layer_id}
        for layer_id, layer in layer_index.items()
    ]

    valid_values = {option["value"] for option in options}
    value = [
        layer_id
        for layer_id in _ensure_list(selected_values)
        if layer_id in valid_values
    ]
    return options, value


# selection


@app.callback(
    Output({"type": "checklist", "index": MATCH}, "value"),
    [
        Input({"type": "checklist", "index": MATCH}, "options"),
        Input({"type": "select-all", "index": MATCH}, "n_clicks"),
        Input({"type": "select-none", "index": MATCH}, "n_clicks"),
    ],
    State({"type": "checklist", "index": MATCH}, "value"),
)
def checklist_selection(options, _n_all, _n_none, current_value, callback_context):
    """Resolve station checklist selection for all/none and refresh events.

    Args:
        options: Checklist options for the matched block.
        _n_all: Click count for the "All" button.
        _n_none: Click count for the "None" button.
        current_value: Currently selected option values.
        callback_context: Dash callback context used to inspect trigger source.

    Returns:
        list: Updated selected values for the matched checklist.
    """
    triggered = (
        callback_context.triggered[0]["prop_id"] if callback_context.triggered else ""
    )
    triggered_component = triggered.rsplit(".", 1)[0]
    option_values = [option["value"] for option in (options or [])]

    if "select-none" in triggered_component:
        return []
    if "select-all" in triggered_component:
        return option_values

    # Keep the current user selection whenever options are refreshed.
    selected_values = [
        value for value in _ensure_list(current_value) if value in set(option_values)
    ]
    if selected_values:
        return selected_values

    return option_values


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
        Input("spatial-layer-checklist", "value"),
        Input("map-style-select", "value"),
    ],
)
def update_map(
    owned_selected,
    public_selected,
    spatial_layer_selected_ids,
    map_style_value,
    callback_context,
    **kwargs,
):
    """Build a scatter-mapbox figure for currently selected stations and layers.

    Args:
        owned_selected: Selected station codes from the owned checklist.
        public_selected: Selected station codes from the public checklist.
        spatial_layer_selected_ids: Checked spatial layer ids from the
            spatial layer checklist.
        map_style_value: Requested map style value.
        callback_context: Dash callback context used to inspect trigger source.
        **kwargs: Callback kwargs containing request context.

    Returns:
        Patch | object: Patch update for the map figure or no_update.
    """
    user = _get_request_user(kwargs)

    valid_styles = {option["value"] for option in _MAP_STYLE_OPTIONS}
    map_style = (
        map_style_value if map_style_value in valid_styles else _DEFAULT_MAP_STYLE
    )

    triggered = (
        callback_context.triggered[0]["prop_id"] if callback_context.triggered else ""
    )
    triggered_component = triggered.rsplit(".", 1)[0]
    is_initial_call = not triggered_component

    patched = Patch()

    if (
        is_initial_call
        or '"type":"checklist"' in triggered_component
        or "'type': 'checklist'" in triggered_component
        or triggered_component == "spatial-layer-checklist"
    ):
        rows = _station_rows_for_codes(owned_selected, "My Stations")
        rows.extend(_station_rows_for_codes(public_selected, "Public"))

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

    if is_initial_call or triggered_component == "spatial-layer-checklist":
        available_layers = available_map_layers_by_id(user)
        selected_layer_ids = [
            layer_id
            for layer_id in _ensure_list(spatial_layer_selected_ids)
            if layer_id in available_layers
        ]
        spatial_layers_raw = [
            {
                "id": layer_id,
                "name": available_layers[layer_id]["name"],
                "source_kind": "geotiff",
                "visible": True,
                "order": order,
            }
            for order, layer_id in enumerate(selected_layer_ids, start=1)
        ]
        patched["layout"]["mapbox"]["layers"] = build_mapbox_layers(
            spatial_layers_raw,
            user,
        )

    if is_initial_call or triggered_component == "map-style-select":
        patched["layout"]["mapbox"]["style"] = map_style

    if patched == {}:
        return no_update

    return patched
