from datetime import datetime
from decimal import Decimal

import plotly.express as px
from dash import dcc, html, Input, Output
from django_plotly_dash import DjangoDash

import pandas as pd

from station.models import Station
from validated.functions import dict_data_report
from variable.models import Variable

# Create a Dash app
app = DjangoDash("DataReport")


# Initial values
station: Station = Station.objects.order_by("station_code")[7]
variable: Variable = Variable.objects.order_by("variable_code")[0]
start_time: str = datetime.strptime("2023-03-01", "%Y-%m-%d")
end_time: str = datetime.strptime("2023-03-31", "%Y-%m-%d")
temporality: str = "measurement"


def plot_graph(
    temporality: str,
    station: Station,
    variable: Variable,
    start_time: str,
    end_time: str,
):
    # Load data
    data: dict = dict_data_report(
        temporality=temporality,
        station=station,
        variable=variable,
        start_time=start_time,
        end_time=end_time,
    )

    # Create plot
    x = data["series"]["time"]
    y = data["series"]["average"]
    plot = px.line(x=x, y=y)

    return plot


plot = plot_graph(
    temporality,
    station,
    variable,
    start_time,
    end_time,
)


# Create layout
app.layout = html.Div([
    dcc.Dropdown(
        id="temporality_drop",
        options=[
            {'label': 'Raw measurement', 'value': 'measurement'},
            {'label': 'Validated measurement', 'value': 'validated'},
            {'label': 'Hourly', 'value': 'hourly'},
            {'label': 'Daily', 'value': 'daily'},
            {'label': 'Monthly', 'value': 'monthly'},
        ],
        value="measurement",
    ),
    dcc.Dropdown(
        id="station_drop",
        #options=Station.objects.order_by("station_code"),
        options=[item.station_code for item in Station.objects.order_by("station_code")],
        value=station.station_code,
    ),
    dcc.Dropdown(
        id="variable_drop",
        options=[{'label': item.name, 'value': item.variable_code} for item in Variable.objects.order_by("variable_code")],
        value=variable.variable_code,
    ),
    dcc.DatePickerRange(
        id="date_range_picker",
        display_format="YYYY-MM-DD",
        start_date="2023-03-01",
        end_date="2023-03-31",
    ),
    dcc.Graph(id="data_report_graph", figure=plot)
])


@app.callback(
    Output("data_report_graph", "figure"),
    [
        Input("temporality_drop", "value"),
        Input("station_drop", "value"),
        Input("variable_drop", "value"),
        Input("date_range_picker", "start_date"),
        Input("date_range_picker", "end_date"),
    ],
)
def update_button_click(
    temporality: str,
    station: str,
    variable: str,
    start_time: str,
    end_time: str,
) -> px.line:

    station = Station.objects.get(station_code=station)
    variable = Variable.objects.get(variable_code=variable)
    
    plot = plot_graph(
        temporality,
        station,
        variable,
        start_time,
        end_time,
    )

    return plot