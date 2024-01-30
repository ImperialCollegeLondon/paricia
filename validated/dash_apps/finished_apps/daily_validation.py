from datetime import datetime
from decimal import Decimal

import plotly.express as px
from dash import dcc, html
from dash.dash_table import DataTable
from dash_ag_grid import AgGrid
from django_plotly_dash import DjangoDash

from station.models import Station
from validated.functions import daily_validation
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

"""
DAILY TABLE
   
"""


def get_columns_daily(value_columns):
    # Essential columns
    always_present_columns = [
        ("id", "Id"),
        ("date", "Date"),
        ("percentage", "Percnt."),
        ("value_difference_error_count", "Diff. Err"),
    ]
    columns = [{"id": id, "name": name} for id, name in always_present_columns]

    # Optional columns
    optional_columns = {
        "sum": "Sum",
        "average": "Average",
        "maximum": "Max. of Maxs.",
        "minimum": "Min. of Mins.",
    }
    columns += [
        {"id": id, "name": name}
        for id, name in optional_columns.items()
        if id in value_columns
    ]

    # Action column
    columns.append({"id": "action", "name": "Action"})
    return columns


def get_style_data_conditional():
    style_date = {
        "if": {"column_id": "date", "filter_query": "{date_error} > 0"},
        "backgroundColor": "red",
    }

    # This isn't working
    style_percentage = {
        "if": {"column_id": "percentage", "filter_query": "{percentage_error} eq true"},
        "backgroundColor": "red",
    }

    style_value_diff = {
        "if": {
            "column_id": "value_difference_error_count",
            "filter_query": "{value_difference_error_count} > 0",
        },
        "backgroundColor": "red",
    }

    style_value = [
        {
            "if": {
                "column_id": "value",
                "filter_query": "{{suspicious_{field}s_count}} > 0".format(field=field),
            },
            "backgroundColor": "red",
        }
        for field in ["sum", "average", "maximum", "minimum"]
    ]

    style_data_conditional = [
        style_date,
        style_percentage,
        style_value_diff,
    ] + style_value
    return style_data_conditional


def create_daily_table_ag(data):
    table = AgGrid(
        id="table",
        data=data["data"],
        columns=get_columns_daily(value_columns=data["value_columns"]),
        rowMultiSelect=True,
        gridOptions={
            "defaultColDef": {
                "cellStyle": get_style_data_conditional(),
            },
        },
    )
    return table


def create_daily_table(data):
    table = DataTable(
        id="table",
        columns=get_columns_daily(value_columns=data["value_columns"]),
        data=data["data"],
        row_selectable="multi",
        style_header={"fontWeight": "bold"},
        style_data_conditional=get_style_data_conditional(),
    )
    return table


table = create_daily_table(data)
# table = create_daily_table_ag(data)

# Create layout
# app.layout = html.Div([dcc.Graph(figure=plot)])
app.layout = html.Div([table])


"""
To do:
- Add action buttons
- Fix percentage column formatting
- Add error counts

"""
