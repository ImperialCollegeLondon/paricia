"""Dash app for selecting stations and rendering them on an interactive map.

This module defines a DjangoDash application with two station checklist sections,
plus a third block for spatial layer controls. GeoTIFF layers are loaded from
MapLayerImport entries and rendered below station points.
"""

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from dash import ALL, MATCH, Input, Output, Patch, State, dcc, html, no_update
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
        dbc.Card: Card containing a layer picker and selected-layer list.
    """
    return dbc.Card(
        [
            dbc.CardHeader("Spatial Data", className="py-2"),
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id="spatial-layer-dropdown",
                        options=[],
                        value=None,
                        placeholder="Add a spatial layer...",
                        clearable=True,
                    ),
                    html.Div(
                        id="spatial-layer-list",
                        className="mt-2",
                        style={
                            "maxHeight": SCROLL_HEIGHT,
                            "overflowY": "auto",
                            "border": "1px solid #dee2e6",
                            "borderRadius": "4px",
                            "padding": "6px 8px",
                        },
                    ),
                    dcc.Store(id="spatial-layer-store", data=[]),
                ],
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


def _normalise_spatial_layer_store(store_data):
    """Normalise layer-store payload to an ordered list of unique entries.

    Args:
        store_data: List-like payload containing layer ids or entry dictionaries.

    Returns:
        list[dict[str, object]]: Entries with ``id`` and ``visible`` keys.
    """
    normalised = []
    seen = set()

    for item in _ensure_list(store_data):
        if isinstance(item, dict):
            layer_id = item.get("id")
            visible = bool(item.get("visible", True))
        else:
            layer_id = item
            visible = True

        if layer_id in (None, "") or layer_id in seen:
            continue

        normalised.append({"id": layer_id, "visible": visible})
        seen.add(layer_id)

    return normalised


def _triggered_component(callback_context):
    """Return component id from django-plotly-dash callback context."""
    triggered_prop = (
        callback_context.triggered[0]["prop_id"] if callback_context.triggered else ""
    )
    return triggered_prop.rsplit(".", 1)[0] if triggered_prop else ""


def _build_spatial_layer_row(layer_id, layer_name, visible):
    """Build one selected-layer row with a visibility toggle and remove button.

    Args:
        layer_id: Map layer identifier used by callbacks.
        layer_name (str): Label shown to the user.
        visible (bool): Whether the layer is currently visible on the map.

    Returns:
        html.Div: Row containing checkbox, name, and a remove button.
    """
    return html.Div(
        [
            dbc.Checkbox(
                id={"type": "spatial-layer-visible", "index": layer_id},
                value=visible,
                className="me-2",
            ),
            html.Span(layer_name, className="flex-grow-1"),
            html.Button(
                "x",
                id={"type": "spatial-layer-remove", "index": layer_id},
                n_clicks=0,
                type="button",
                className="btn btn-link text-danger p-0 ms-2",
                title=f"Remove {layer_name}",
            ),
        ],
        className="d-flex align-items-center py-1 border-bottom",
    )


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
        Output("spatial-layer-store", "data"),
        Output("spatial-layer-dropdown", "options"),
        Output("spatial-layer-dropdown", "value"),
        Output("spatial-layer-list", "children"),
    ],
    [
        Input("stations_list", "children"),
        Input("map-style-select", "value"),
        Input("spatial-layer-dropdown", "value"),
        Input({"type": "spatial-layer-remove", "index": ALL}, "n_clicks"),
        Input({"type": "spatial-layer-visible", "index": ALL}, "value"),
    ],
    [
        State({"type": "spatial-layer-remove", "index": ALL}, "id"),
        State({"type": "spatial-layer-visible", "index": ALL}, "id"),
        State("spatial-layer-store", "data"),
    ],
)
def sync_spatial_layer_controls(
    _stations_raw,
    _map_style_value,
    dropdown_layer_id,
    _remove_clicks,
    visibility_values,
    remove_ids,
    visibility_ids,
    store_data,
    callback_context,
    **kwargs,
):
    """Sync spatial-layer picker, selected-list rows, and map visibility state.

    Args:
        _stations_raw: Unused trigger input for station list changes.
        _map_style_value: Current map style value.
        dropdown_layer_id: Layer id selected from the add-layer dropdown.
        _remove_clicks: Click counts from per-layer remove buttons.
        visibility_values: Visibility booleans for selected layer checkboxes.
        remove_ids: Pattern-matching ids for the remove buttons.
        visibility_ids: Pattern-matching ids for the visibility checkboxes.
        store_data: Current selected-layer store payload.
        callback_context: Dash callback context used to inspect trigger source.
        **kwargs: Callback kwargs containing request context.

    Returns:
        tuple[list[dict], list[dict], None, list[html.Div]]: Selected layer
            store data, add-layer dropdown options, reset dropdown value, and
            selected-layer row components.
    """
    user = _get_request_user(kwargs)
    layer_index = available_map_layers_by_id(user)
    selected_layers = [
        entry
        for entry in _normalise_spatial_layer_store(store_data)
        if entry["id"] in layer_index
    ]

    triggered_component = _triggered_component(callback_context)

    if triggered_component == "map-style-select":
        selected_layers = []
    elif triggered_component == "spatial-layer-dropdown":
        selected_layer_ids = {entry["id"] for entry in selected_layers}
        if (
            dropdown_layer_id in layer_index
            and dropdown_layer_id not in selected_layer_ids
        ):
            # New layers start unchecked and only show once user enables them.
            selected_layers.append({"id": dropdown_layer_id, "visible": False})
    elif '"type":"spatial-layer-remove"' in triggered_component:
        clicked_remove_ids = [
            (button_id.get("index"), clicks)
            for button_id, clicks in zip(
                _ensure_list(remove_ids),
                _ensure_list(_remove_clicks),
            )
            if isinstance(button_id, dict) and clicks
        ]
        removed_id = (
            max(clicked_remove_ids, key=lambda item: item[1])[0]
            if clicked_remove_ids
            else None
        )

        selected_layers = [
            entry for entry in selected_layers if entry["id"] != removed_id
        ]
    elif '"type":"spatial-layer-visible"' in triggered_component:
        visibility_by_id = {
            visibility_id.get("index"): bool(value)
            for visibility_id, value in zip(
                _ensure_list(visibility_ids),
                _ensure_list(visibility_values),
            )
            if isinstance(visibility_id, dict) and "index" in visibility_id
        }
        selected_layers = [
            {
                "id": entry["id"],
                "visible": visibility_by_id.get(entry["id"], entry["visible"]),
            }
            for entry in selected_layers
        ]

    selected_layer_ids = {entry["id"] for entry in selected_layers}
    dropdown_options = [
        {"label": layer["name"], "value": layer_id}
        for layer_id, layer in layer_index.items()
        if layer_id not in selected_layer_ids
    ]

    layer_rows = [
        _build_spatial_layer_row(
            entry["id"],
            layer_index[entry["id"]]["name"],
            entry["visible"],
        )
        for entry in selected_layers
    ]
    if not layer_rows:
        layer_rows = [
            html.Div(
                "No spatial layers selected.",
                className="text-muted fst-italic small",
            )
        ]

    return selected_layers, dropdown_options, None, layer_rows


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
    triggered_component = _triggered_component(callback_context)
    option_values = [option["value"] for option in (options or [])]

    if "select-none" in triggered_component:
        return []
    if "select-all" in triggered_component:
        return option_values

    # Keep the current user selection whenever options are refreshed.
    option_values_set = set(option_values)
    selected_values = [
        value for value in _ensure_list(current_value) if value in option_values_set
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
        Input("spatial-layer-store", "data"),
        Input("map-style-select", "value"),
    ],
)
def update_map(
    owned_selected,
    public_selected,
    spatial_layer_store,
    map_style_value,
    callback_context,
    **kwargs,
):
    """Build a scatter-mapbox figure for currently selected stations and layers.

    Args:
        owned_selected: Selected station codes from the owned checklist.
        public_selected: Selected station codes from the public checklist.
        spatial_layer_store: Selected spatial layers and their visibility.
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

    triggered_component = _triggered_component(callback_context)
    is_initial_call = not triggered_component

    patched = Patch()

    if (
        is_initial_call
        or '"type":"checklist"' in triggered_component
        or triggered_component == "spatial-layer-store"
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

    if is_initial_call or triggered_component == "spatial-layer-store":
        available_layers = available_map_layers_by_id(user)
        spatial_layers_raw = [
            {"id": entry["id"], "visible": True}
            for entry in _normalise_spatial_layer_store(spatial_layer_store)
            if entry["visible"] and entry["id"] in available_layers
        ]
        patched["layout"]["mapbox"]["layers"] = build_mapbox_layers(
            spatial_layers_raw,
            user,
        )

    if is_initial_call or triggered_component == "map-style-select":
        patched["layout"]["mapbox"]["style"] = map_style
    if triggered_component == "map-style-select":
        patched["layout"]["mapbox"]["layers"] = []

    if patched == {}:
        return no_update

    return patched
