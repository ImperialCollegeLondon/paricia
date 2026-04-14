"""Dash app for selecting stations and rendering them on an interactive map.

This module defines a DjangoDash application with two checklist sections
(owned and public stations), bulk selection controls, and a map view updated
from current checklist selections.
"""

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Input, Output, State, dcc, html
from django.forms.models import model_to_dict
from django_plotly_dash import DjangoDash

from station.models import Station

SCROLL_HEIGHT = "280px"

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
            id=f"{block_id}-checklist",
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
                id=f"{block_id}-select-all",
                size="sm",
                color="secondary",
                outline=True,
            ),
            dbc.Button(
                "None",
                id=f"{block_id}-select-none",
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


_sidebar = dbc.Col(
    [
        html.H6("Stations", className="fw-bold mb-3 mt-3 ps-1"),
        html.Div(_station_block("owned", "My Stations"), id="owned-block"),
        _station_block("public", "Public Stations"),
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
    dcc.Graph(id="map_graph", style={"height": "100vh"}, config={"scrollZoom": True}),
    width=9,
    style={"padding": "0"},
)

app.layout = dbc.Container(
    fluid=True,
    style={"height": "100vh", "padding": "0"},
    children=[
        dbc.Row([_sidebar, _map_col], className="g-0"),
        html.Div(id="stations_list", style={"display": "none"}),
        dcc.Store(id="owned-btn-store", data={"n_all": 0, "n_none": 0}),
        dcc.Store(id="public-btn-store", data={"n_all": 0, "n_none": 0}),
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
    options = []
    for code in sorted(codes):
        try:
            obj = Station.objects.get(station_code=code)
            label = f"{code} \u2013 {obj.station_name}" if obj.station_name else code
        except Station.DoesNotExist:
            label = code
        options.append({"label": label, "value": code})
    return options


# ── Populate checklist options ────────────────────────────────────────────────


@app.callback(
    [
        Output("owned-checklist", "options"),
        Output("public-checklist", "options"),
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


# ── Owned selection ───────────────────────────────────────────────────────────


@app.callback(
    Output("owned-checklist", "value"),
    [
        Input("owned-checklist", "options"),
        Input("owned-select-all", "n_clicks"),
        Input("owned-select-none", "n_clicks"),
    ],
    State("owned-btn-store", "data"),
)
def owned_selection(options, n_all, n_none, store):
    """Resolve the selected values for the owned stations checklist.

    All options are selected by default.  The selection is cleared only when
    the *None* button click count has increased since it was last stored.

    Args:
        options (list[dict] | None): Current checklist options.
        n_all (int | None): Total click count for the *All* button.
        n_none (int | None): Total click count for the *None* button.
        store (dict | None): Previously stored click counts.

    Returns:
        list[str]: Station codes to mark as selected.
    """
    options = options or []
    if (n_none or 0) > (store or {}).get("n_none", 0):
        return []
    return [o["value"] for o in options]


@app.callback(
    Output("owned-btn-store", "data"),
    [
        Input("owned-select-all", "n_clicks"),
        Input("owned-select-none", "n_clicks"),
    ],
)
def owned_store(n_all, n_none):
    """Persist the owned checklist bulk-button click counters.

    Args:
        n_all (int | None): Total click count for the *All* button.
        n_none (int | None): Total click count for the *None* button.

    Returns:
        dict[str, int]: Updated click counters for use as callback state.
    """
    return {"n_all": n_all or 0, "n_none": n_none or 0}


# ── Public selection ──────────────────────────────────────────────────────────


@app.callback(
    Output("public-checklist", "value"),
    [
        Input("public-checklist", "options"),
        Input("public-select-all", "n_clicks"),
        Input("public-select-none", "n_clicks"),
    ],
    State("public-btn-store", "data"),
)
def public_selection(options, n_all, n_none, store):
    """Resolve the selected values for the public stations checklist.

    All options are selected by default.  The selection is cleared only when
    the *None* button click count has increased since it was last stored.

    Args:
        options (list[dict] | None): Current checklist options.
        n_all (int | None): Total click count for the *All* button.
        n_none (int | None): Total click count for the *None* button.
        store (dict | None): Previously stored click counts.

    Returns:
        list[str]: Station codes to mark as selected.
    """
    options = options or []
    if (n_none or 0) > (store or {}).get("n_none", 0):
        return []
    return [o["value"] for o in options]


@app.callback(
    Output("public-btn-store", "data"),
    [
        Input("public-select-all", "n_clicks"),
        Input("public-select-none", "n_clicks"),
    ],
)
def public_store(n_all, n_none):
    """Persist the public checklist bulk-button click counters.

    Args:
        n_all (int | None): Total click count for the *All* button.
        n_none (int | None): Total click count for the *None* button.

    Returns:
        dict[str, int]: Updated click counters for use as callback state.
    """
    return {"n_all": n_all or 0, "n_none": n_none or 0}


# ── Map ───────────────────────────────────────────────────────────────────────

_COLOR_MAP = {
    "My Stations": "#e74c3c",
    "Public": "#3498db",
}


@app.callback(
    Output("map_graph", "figure"),
    [
        Input("owned-checklist", "value"),
        Input("public-checklist", "value"),
    ],
)
def update_map(owned_selected, public_selected):
    """Build a scatter-mapbox figure for the currently selected stations.

    Owned and public stations are rendered in different colours defined by
    ``_COLOR_MAP``.  When no stations are selected an empty basemap is
    returned so the tile layer remains visible.

    Args:
        owned_selected (list[str] | None): Station codes selected in the
            owned group.
        public_selected (list[str] | None): Station codes selected in the
            public group.

    Returns:
        plotly.graph_objects.Figure: Scatter-mapbox figure coloured by station
            group, or a blank basemap when the selection is empty.
    """
    keys = [
        "station_id",
        "station_code",
        "station_name",
        "station_latitude",
        "station_longitude",
    ]

    rows = []
    for code in owned_selected or []:
        row = {
            k: model_to_dict(Station.objects.get(station_code=code))[k] for k in keys
        }
        row["type"] = "My Stations"
        rows.append(row)
    for code in public_selected or []:
        row = {
            k: model_to_dict(Station.objects.get(station_code=code))[k] for k in keys
        }
        row["type"] = "Public"
        rows.append(row)

    base_layout = {
        "mapbox": {"style": "open-street-map", "zoom": 3.6},
        "margin": {"r": 0, "t": 0, "l": 0, "b": 0},
        "legend": {
            "title": "",
            "x": 0.01,
            "y": 0.99,
            "bgcolor": "rgba(255,255,255,0.8)",
        },
    }

    if not rows:
        return px.scatter_mapbox(lat=[], lon=[]).update_layout(**base_layout)

    df = pd.DataFrame(rows, columns=[*keys, "type"])
    plot = px.scatter_mapbox(
        df,
        lat="station_latitude",
        lon="station_longitude",
        hover_name="station_code",
        color="type",
        color_discrete_map=_COLOR_MAP,
        category_orders={"type": list(_COLOR_MAP)},
        zoom=3.6,
    )
    plot.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend={"title": "", "x": 0.01, "y": 0.99, "bgcolor": "rgba(255,255,255,0.8)"},
    )
    return plot
