from datetime import datetime
from decimal import Decimal
import plotly.express as px
from dash import dcc, html
from django_plotly_dash import DjangoDash

from station.models import Station
from variable.models import Variable
from validated.functions import daily_validation

# Create a Dash app
app = DjangoDash("DailyValidation")

# Filters (in final app this will get data from forms)
station: Station = Station.objects.order_by("station_code")[7]
variable: Variable = Variable.objects.order_by("variable_code")[0]
start_time: datetime = datetime.strptime("2023-03-01", "%Y-%m-%d")
end_time: datetime = datetime.strptime("2023-03-31", "%Y-%m-%d")
minimum: Decimal = Decimal(-5)
maximum: Decimal = Decimal(28)

# Load data
data: dict = daily_validation(
    station=station,
    variable=variable,
    start_time=start_time,
    end_time=end_time,
    minimum=minimum,
    maximum=maximum,
)

# Create plot
x = data["series"]["measurement"]["time"]
y = data["series"]["measurement"]["average"]
plot = px.line(x=x, y=y)

# Create layout
app.layout = html.Div([dcc.Graph(figure=plot)])
