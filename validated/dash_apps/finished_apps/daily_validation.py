from datetime import datetime
from decimal import Decimal

import plotly.graph_objects as go
from dash import dcc, html
from django_plotly_dash import DjangoDash

from station.models import Station
from validated.functions import daily_validation, detail_list
from validated.tables import create_daily_table, create_detail_table
from variable.models import Variable

DEFAULT_FONT = "Open Sans, Raleway, Dosis, Ubuntu, sans-serif"

app = DjangoDash("DailyValidation")

# Filters (in final app this will get data from forms)
station: Station = Station.objects.order_by("station_code")[7]
variable: Variable = Variable.objects.order_by("variable_code")[0]
start_time: datetime = datetime.strptime("2023-03-01", "%Y-%m-%d")
end_time: datetime = datetime.strptime("2023-03-31", "%Y-%m-%d")
minimum: Decimal = Decimal(-5)
maximum: Decimal = Decimal(28)

# Daily data
data: dict = daily_validation(
    station=station,
    variable=variable,
    start_time=start_time,
    end_time=end_time,
    minimum=minimum,
    maximum=maximum,
)

# Detail data
date: datetime = datetime.strptime("2023-03-14", "%Y-%m-%d")
data_detail = detail_list(
    station=station,
    variable=variable,
    date_of_interest=date,
    minimum=minimum,
    maximum=maximum,
)


# Plot
plot = go.Figure()
plot.add_trace(
    go.Scatter(
        x=data["series"]["measurement"]["time"],
        y=data["series"]["measurement"]["average"],
        mode="lines",
        name="Measurement",
        line=dict(color="black"),
    )
)
plot.add_trace(
    go.Scatter(
        x=data["series"]["selected"]["time"],
        y=data["series"]["selected"]["average"],
        mode="lines",
        name="Selected",
        line=dict(color="#636EFA"),
    )
)
plot.add_trace(
    go.Scatter(
        x=data["series"]["validated"]["time"],
        y=data["series"]["validated"]["average"],
        mode="lines",
        name="Validated",
        line=dict(color="#00CC96"),
    )
)

# Tables
table_daily = create_daily_table(data)
table_detail = create_detail_table(data_detail)

# Layout
app.layout = html.Div(
    children=[
        html.H1(
            children="Daily Report",
            style={"font-family": DEFAULT_FONT},
        ),
        table_daily,
        html.H1(
            children="Detail of Selected Day",
            style={"font-family": DEFAULT_FONT},
        ),
        table_detail,
        html.H1(
            children="Plot",
            style={"font-family": DEFAULT_FONT},
        ),
        dcc.Graph(figure=plot),
    ]
)
