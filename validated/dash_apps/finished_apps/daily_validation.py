from datetime import datetime
from decimal import Decimal

import plotly.graph_objects as go
from dash import dcc, html
from django_plotly_dash import DjangoDash

from station.models import Station
from validated.functions import daily_validation, detail_list
from validated.tables import create_daily_table, create_detail_table
from variable.models import Variable

# Create a Dash app
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
    )
)
plot.add_trace(
    go.Scatter(
        x=data["series"]["validated"]["time"],
        y=data["series"]["validated"]["average"],
        mode="lines",
        name="Validated",
    )
)
plot.add_trace(
    go.Scatter(
        x=data["series"]["selected"]["time"],
        y=data["series"]["selected"]["average"],
        mode="lines",
        name="Selected",
    )
)

# Tables
table_daily = create_daily_table(data)
table_detail = create_detail_table(data_detail)

# Layout
app.layout = html.Div([table_daily, table_detail, dcc.Graph(figure=plot)])

# Callback: check boxes


"""
To do:
- Reformat time column

"""
