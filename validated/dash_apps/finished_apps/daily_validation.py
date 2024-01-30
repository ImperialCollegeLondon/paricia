from datetime import datetime
from decimal import Decimal

import plotly.express as px
from dash import dcc, html
from dash_ag_grid import AgGrid
from django_plotly_dash import DjangoDash

from station.models import Station
from validated.functions import daily_validation, detail_list
from variable.models import Variable

# Create a Dash app
app = DjangoDash("DailyValidation")

"""
DAILY DATA

"""

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

"""
DETAIL DATA

"""

date: datetime = datetime.strptime("2023-03-14", "%Y-%m-%d")

data_detail = detail_list(
    station=station,
    variable=variable,
    date_of_interest=date,
    minimum=minimum,
    maximum=maximum,
)

"""
PLOT

"""

x = data["series"]["measurement"]["time"]
y = data["series"]["measurement"]["average"]
plot = px.line(x=x, y=y)

"""
DAILY TABLE
   
"""


def get_columns_daily(value_columns):
    styles = get_style_data_conditional()

    # Essential columns
    essental_columns = [
        {"field": "id", "headerName": "Id"},
        {"field": "date", "headerName": "Date", **styles["date"]},
        {"field": "percentage", "headerName": "Percnt.", **styles["percentage"]},
        {
            "field": "value_difference_error_count",
            "headerName": "Diff. Err",
            **styles["value_difference_error_count"],
        },
    ]

    # Optional columns
    optional_columns = [
        {"field": "sum", "headerName": "Sum"},
        {"field": "average", "headerName": "Average", **styles["average"]},
        {"field": "maximum", "headerName": "Max. of Maxs.", **styles["maximum"]},
        {"field": "minimum", "headerName": "Min. of Mins.", **styles["minimum"]},
    ]

    columns = essental_columns
    columns += [d for d in optional_columns if d["field"] in value_columns]

    # Action column
    columns.append({"field": "action", "headerName": "Action"})
    return columns


def get_style_data_conditional():
    styles = {}

    styles["date"] = {
        "cellStyle": {
            "styleConditions": [
                {
                    "condition": "params.data['date_error'] > 0",
                    "style": {"backgroundColor": "sandybrown"},
                },
            ]
        },
    }

    styles["percentage"] = {
        "cellStyle": {
            "styleConditions": [
                {
                    "condition": "params.data['percentage_error']",
                    "style": {"backgroundColor": "sandybrown"},
                },
            ]
        },
    }

    styles["value_difference_error_count"] = {
        "cellStyle": {
            "styleConditions": [
                {
                    "condition": "params.data['value_difference_error_count'] > 0",
                    "style": {"backgroundColor": "sandybrown"},
                },
            ]
        },
    }

    for field in ["sum", "average", "maximum", "minimum"]:
        styles[field] = {
            "cellStyle": {
                "styleConditions": [
                    {
                        "condition": f"params.data['suspicious_{field}s_count'] > 0",
                        "style": {"backgroundColor": "sandybrown"},
                    },
                ]
            },
        }

    return styles


def create_daily_table(data):
    table_data = data["data"].copy()
    for d in table_data:
        d["action"] = "Action"

    table = AgGrid(
        id="table",
        rowData=table_data,
        columnDefs=get_columns_daily(value_columns=data["value_columns"]),
        columnSize="sizeToFit",
        defaultColDef={
            "resizable": False,
            "sortable": True,
            "filter": False,
            "checkboxSelection": {
                "function": "params.column == params.columnApi.getAllDisplayedColumns()[0]"
            },
            "headerCheckboxSelection": {
                "function": "params.column == params.columnApi.getAllDisplayedColumns()[0]"
            },
        },
        dashGridOptions={"rowSelection": "multiple", "suppressRowClickSelection": True},
    )
    return table


"""
DETAIL TABLE

"""


"""
LAYOUT

"""

# table = create_daily_table(data)
table = create_daily_table(data)

# Create layout
app.layout = html.Div([table, dcc.Graph(figure=plot)])


"""
To do:
- Add action buttons
- Add error counts
- Have chackboxes selected by default

"""
