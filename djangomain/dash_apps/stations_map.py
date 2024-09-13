import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html
from django.forms.models import model_to_dict
from django_plotly_dash import DjangoDash

from station.models import Station

# Create a Dash app
app = DjangoDash(
    "StationsMap",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)


# Create layout
app.layout = html.Div(
    children=[
        html.Div(id="test_list"),
        dcc.Graph(
            id="map_graph",
            style={"display": "none"},
        ),
        html.Div(id="stations_list", style={"display": "none"}),
    ]
)


@app.callback(
    [
        Output("map_graph", "figure"),
        Output("map_graph", "style"),
    ],
    Input("stations_list", "children"),
)
def update_map(stations) -> px.line:
    station_objs = [
        model_to_dict(Station.objects.get(station_code=code)) for code in stations
    ]

    keys = [
        "station_id",
        "station_code",
        "station_name",
        "station_latitude",
        "station_longitude",
    ]

    stations_filtered = [{key: obj[key] for key in keys} for obj in station_objs]

    df = pd.DataFrame(stations_filtered, columns=keys)
    plot = px.scatter_mapbox(
        df,
        lat="station_latitude",
        lon="station_longitude",
        hover_name="station_code",
        zoom=3.6,
    )
    plot.update_layout(mapbox_style="open-street-map")
    plot.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return plot, {"display": "block"}
