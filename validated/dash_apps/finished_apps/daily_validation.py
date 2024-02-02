from datetime import datetime
from decimal import Decimal

import dash
import plotly.graph_objects as go
from dash import Input, Output, State, dcc, html
from dash_ag_grid import AgGrid
from django_plotly_dash import DjangoDash

from station.models import Station
from validated.functions import (
    daily_validation,
    detail_list,
    get_conditions,
    reset_daily_validated,
    reset_detail_validated,
    save_detail_to_validated,
    save_to_validated,
)
from validated.tables import create_columns_daily, create_columns_detail
from variable.models import Variable

DEFAULT_FONT = "Open Sans, Raleway, Dosis, Ubuntu, sans-serif"

app = DjangoDash("DailyValidation")

# Filters (in final app this will get data from forms)
station: Station = Station.objects.order_by("station_code")[7]
variable: Variable = Variable.objects.order_by("variable_code")[0]
start_date: datetime = datetime.strptime("2023-03-01", "%Y-%m-%d")
end_date: datetime = datetime.strptime("2023-03-31", "%Y-%m-%d")
minimum: Decimal = Decimal(-5)
maximum: Decimal = Decimal(28)
selected_day: datetime = datetime.strptime("2023-03-14", "%Y-%m-%d")

# Daily data
data_daily = daily_validation(
    station=station,
    variable=variable,
    start_time=start_date,
    end_time=end_date,
    minimum=minimum,
    maximum=maximum,
)

# Detail data
data_detail = detail_list(
    station=station,
    variable=variable,
    date_of_interest=selected_day,
    minimum=minimum,
    maximum=maximum,
)

# Tables
table_daily = AgGrid(
    id="table_daily",
    rowData=data_daily["data"],
    columnDefs=create_columns_daily(value_columns=data_daily["value_columns"]),
    columnSize="sizeToFit",
    defaultColDef={
        "resizable": True,
        "sortable": True,
        "checkboxSelection": {
            "function": "params.column == params.columnApi.getAllDisplayedColumns()[0]"
        },
        "headerCheckboxSelection": {
            "function": "params.column == params.columnApi.getAllDisplayedColumns()[0]"
        },
        "headerCheckboxSelectionFilteredOnly": True,
    },
    dashGridOptions={"rowSelection": "multiple", "suppressRowClickSelection": True},
    selectAll=True,
)

table_detail = AgGrid(
    id="table_detail",
    rowData=data_detail["series"],
    columnDefs=create_columns_detail(value_columns=data_detail["value_columns"]),
    columnSize="sizeToFit",
    defaultColDef={
        "resizable": True,
        "sortable": True,
        "checkboxSelection": {
            "function": "params.column == params.columnApi.getAllDisplayedColumns()[0]"
        },
        "headerCheckboxSelection": {
            "function": "params.column == params.columnApi.getAllDisplayedColumns()[0]"
        },
        "headerCheckboxSelectionFilteredOnly": True,
    },
    dashGridOptions={"rowSelection": "multiple", "suppressRowClickSelection": True},
    selectAll=True,
)


# Plot
def create_validation_plot(data: dict) -> go.Figure:
    """Creates plot for Validation app

    Args:
        data (dict): Daily data

    Returns:
        go.Figure: Plot
    """
    plot = go.Figure()

    datasets = [
        {"key": "measurement", "name": "Measurement", "color": "black"},
        {"key": "selected", "name": "Selected", "color": "#636EFA"},
        {"key": "validated", "name": "Validated", "color": "#00CC96"},
    ]

    for dataset in datasets:
        plot.add_trace(
            go.Scatter(
                x=data["series"][dataset["key"]]["time"],
                y=data["series"][dataset["key"]]["average"],
                name=dataset["name"],
                line=dict(color=dataset["color"]),
            )
        )

    return plot


plot = create_validation_plot(data=data_daily)

# Layout
app.layout = html.Div(
    children=[
        html.H1(
            children="Daily Report",
            style={"font-family": DEFAULT_FONT},
        ),
        table_daily,
        html.Button("Save to Validated", id="daily-save-button"),
        html.Button("Reset Validated", id="daily-reset-button"),
        html.Div(
            id="daily-status-message",
            children=[""],
            style={"font-family": DEFAULT_FONT},
        ),
        html.H1(
            children="Detail of Selected Day",
            style={"font-family": DEFAULT_FONT},
        ),
        table_detail,
        html.Button("Save to Validated", id="detail-save-button"),
        html.Button("Reset Validated", id="detail-reset-button"),
        html.Div(
            id="detail-status-message",
            children=[""],
            style={"font-family": DEFAULT_FONT},
        ),
        html.H1(
            children="Plot",
            style={"font-family": DEFAULT_FONT},
        ),
        dcc.Graph(id="plot", figure=plot),
    ]
)


@app.callback(
    [
        Output("daily-status-message", "children"),
        Output("detail-status-message", "children"),
        Output("plot", "figure"),
    ],
    [
        Input("daily-save-button", "n_clicks"),
        Input("daily-reset-button", "n_clicks"),
        Input("detail-save-button", "n_clicks"),
        Input("detail-reset-button", "n_clicks"),
    ],
    [
        State("table_daily", "selectedRows"),
        State("table_detail", "selectedRows"),
        State("table_detail", "rowData"),
    ],
    prevent_initial_call=True,
)
def combined_callback(
    daily_save_clicks,
    daily_reset_clicks,
    detail_save_clicks,
    detail_reset_clicks,
    daily_selected_rows,
    detail_selected_rows,
    detail_row_data,
):
    global data_detail
    global data_daily

    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Daily save
    if button_id == "daily-save-button" and daily_selected_rows is not None:
        conditions = get_conditions(daily_selected_rows)
        save_to_validated(
            variable=variable,
            station=station,
            to_delete=conditions,
            start_date=start_date,
            end_date=end_date,
            minimum=minimum,
            maximum=maximum,
        )
        daily_status = f"{len(daily_selected_rows)} entries saved to Validated"
        detail_status = dash.no_update

    # Daily reset
    elif button_id == "daily-reset-button":
        reset_daily_validated(
            variable=variable,
            station=station,
            start_date=start_date,
            end_date=end_date,
        )
        daily_status = "Validation reset"
        detail_status = dash.no_update

    # Detail save
    elif button_id == "detail-save-button" and detail_selected_rows is not None:
        selected_ids = {row["id"] for row in detail_selected_rows}
        for row in detail_row_data:
            row["is_selected"] = row["id"] in selected_ids
        save_detail_to_validated(
            data_list=detail_row_data,
            variable=variable,
            station=station,
        )

        daily_status = dash.no_update
        detail_status = f"{len(detail_selected_rows)} entries saved to Validated"

    # Detail reset
    elif button_id == "detail-reset-button":
        reset_detail_validated(
            data_list=detail_row_data,
            variable=variable,
            station=station,
        )

        daily_status = dash.no_update
        detail_status = "Validation reset"

    else:
        daily_status = dash.no_update
        detail_status = dash.no_update

    # Reload data and redraw plot
    data_daily = daily_validation(
        station=station,
        variable=variable,
        start_time=start_date,
        end_time=end_date,
        minimum=minimum,
        maximum=maximum,
    )
    figure = create_validation_plot(data_daily)
    return daily_status, detail_status, figure
