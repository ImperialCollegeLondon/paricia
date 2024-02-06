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

STATION: Station = Station.objects.order_by("station_code")[7]
VARIABLE: Variable = Variable.objects.order_by("variable_code")[0]
START_DATE: datetime = datetime.strptime("2023-03-01", "%Y-%m-%d")
END_DATE: datetime = datetime.strptime("2023-03-31", "%Y-%m-%d")
MINIMUM: Decimal = Decimal(-5)
MAXIMUM: Decimal = Decimal(28)
SELECTED_DAY: datetime = datetime.strptime("2023-03-14", "%Y-%m-%d")

# Daily data
DATA_DAILY = daily_validation(
    station=STATION,
    variable=VARIABLE,
    start_time=START_DATE,
    end_time=END_DATE,
    minimum=MINIMUM,
    maximum=MAXIMUM,
)

# Detail data
DATA_DETAIL = detail_list(
    station=STATION,
    variable=VARIABLE,
    date_of_interest=SELECTED_DAY,
    minimum=MINIMUM,
    maximum=MAXIMUM,
)

# Tables
table_daily = AgGrid(
    id="table_daily",
    rowData=DATA_DAILY["data"],
    columnDefs=create_columns_daily(value_columns=DATA_DAILY["value_columns"]),
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
    dashGridOptions={
        "rowSelection": "multiple",
        "suppressRowClickSelection": True,
    },
    selectAll=True,
    getRowId="params.data.id",
)

table_detail = AgGrid(
    id="table_detail",
    rowData=DATA_DETAIL["series"],
    columnDefs=create_columns_detail(value_columns=DATA_DETAIL["value_columns"]),
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
    dashGridOptions={
        "rowSelection": "multiple",
        "suppressRowClickSelection": True,
    },
    selectAll=True,
    getRowId="params.data.id",
)


# Plot
def create_validation_plot(data: dict) -> go.Figure:
    """Creates plot for Validation app

    Args:
        data (dict): Daily data series

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
                x=data[dataset["key"]]["time"],
                y=data[dataset["key"]]["average"],
                name=dataset["name"],
                line=dict(color=dataset["color"]),
                mode="markers",
                marker_size=3,
            )
        )

    return plot


plot = create_validation_plot(data=DATA_DAILY["series"])

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
            children=["Open detailed view:"],
            style={"font-family": DEFAULT_FONT},
        ),
        dcc.Input(
            id="input-daily-id",
            type="number",
            debounce=True,
            placeholder="ID",
        ),
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
        html.Button("Add row", id="detail-add-button"),
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
        Output("table_daily", "rowData"),
        Output("table_detail", "rowData"),
        Output("table_detail", "rowTransaction"),
        Output("table_detail", "scrollTo"),
        Output("table_daily", "selectedRows"),
        Output("table_detail", "selectedRows"),
    ],
    [
        Input("daily-save-button", "n_clicks"),
        Input("daily-reset-button", "n_clicks"),
        Input("detail-save-button", "n_clicks"),
        Input("detail-reset-button", "n_clicks"),
        Input("detail-add-button", "n_clicks"),
        Input("input-daily-id", "value"),
    ],
    [
        State("table_daily", "selectedRows"),
        State("table_daily", "rowData"),
        State("table_detail", "selectedRows"),
        State("table_detail", "rowData"),
    ],
    prevent_initial_call=True,
)
def callbacks(
    daily_save_clicks: int,
    daily_reset_clicks: int,
    detail_save_clicks: int,
    detail_reset_clicks: int,
    detail_add_clicks: int,
    daily_id: int,
    in_daily_selected_rows: list[dict],
    in_daily_row_data: list[dict],
    in_detail_selected_rows: list[dict],
    in_detail_row_data: list[dict],
) -> tuple[
    str,
    str,
    go.Figure,
    list[dict],
    list[dict],
    dict,
    dict,
    list[dict],
    list[dict],
]:
    """Callback for buttons adding and resetting Validated data

    Args:
        daily_save_clicks (int): Number of times daily-save-button was clicked
        daily_reset_clicks (int): Number of times daily-reset-button was clicked
        detail_save_clicks (int): Number of times detail-save-button was clicked
        detail_reset_clicks (int): Number of times detail-reset-button was clicked
        detail_add_clicks (int): Number of times detail-add-button was clicked
        in_daily_selected_rows (list[dict]): Selected rows in table_daily
        in_detail_selected_rows (list[dict]): Selected rows in table_detail
        in_detail_row_data (list[dict]): Full row data for table_detail

    Returns:
        tuple[str, str, go.Figure, list[dict], list[dict], dict, dict, list[dict], list[dict]]:
            Callback outputs
    """
    global DATA_DAILY, DATA_DETAIL, SELECTED_DAY

    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    out_daily_status = dash.no_update
    out_detail_status = dash.no_update
    out_plot = dash.no_update
    out_daily_row_data = dash.no_update
    out_detail_row_data = dash.no_update
    out_detail_row_transaction = dash.no_update
    out_detail_scroll = dash.no_update
    out_daily_selected_rows = dash.no_update
    out_detail_selected_rows = dash.no_update

    daily_refresh_required = False
    detail_refresh_required = False
    daily_reset_selection = False
    detail_reset_selection = False
    plot_refresh_required = False

    # Button: Daily save
    if button_id == "daily-save-button":
        selected_ids = {row["id"] for row in in_daily_selected_rows}
        for row in in_daily_row_data:
            row["state"] = row["id"] in selected_ids
        conditions = get_conditions(in_daily_row_data)
        save_to_validated(
            variable=VARIABLE,
            station=STATION,
            to_delete=conditions,
            start_date=START_DATE,
            end_date=END_DATE,
            minimum=MINIMUM,
            maximum=MAXIMUM,
        )
        out_daily_status = f"{len(in_daily_selected_rows)} days saved to Validated"
        plot_refresh_required = True
        daily_refresh_required = True

    # Button: Daily reset
    elif button_id == "daily-reset-button":
        reset_daily_validated(
            variable=VARIABLE,
            station=STATION,
            start_date=START_DATE,
            end_date=END_DATE,
        )
        out_daily_status = "Validation reset"
        plot_refresh_required = True
        daily_refresh_required = True
        daily_reset_selection = True

    # Button: Detail save
    elif button_id == "detail-save-button":
        selected_ids = {row["id"] for row in in_detail_selected_rows}
        for row in in_detail_row_data:
            row["is_selected"] = row["id"] in selected_ids
        save_detail_to_validated(
            data_list=in_detail_row_data,
            variable=VARIABLE,
            station=STATION,
        )
        out_detail_status = f"{len(in_detail_selected_rows)} entries saved to Validated"
        plot_refresh_required = True
        detail_refresh_required = True

    # Button: Detail reset
    elif button_id == "detail-reset-button":
        reset_detail_validated(
            data_list=in_detail_row_data,
            variable=VARIABLE,
            station=STATION,
        )
        out_detail_status = "Validation reset"
        plot_refresh_required = True
        detail_refresh_required = True
        detail_reset_selection = True

    # Button: Detail new row
    elif button_id == "detail-add-button":
        last_id = in_detail_row_data[-1]["id"]
        last_time = in_detail_row_data[-1]["time"]
        new_row = {
            "id": last_id + 1,
            "time": last_time,
            **{key: None for key in DATA_DAILY["value_columns"]},
            "outlier": False,
            "value_difference": None,
            "is_selected": False,
        }
        out_detail_row_transaction = {"add": [new_row]}
        out_detail_scroll = {"data": new_row}

    # Input: Daily date
    elif button_id == "input-daily-id":
        SELECTED_DAY = next(
            (d["date"] for d in DATA_DAILY["data"] if d["id"] == daily_id),
            dash.no_update,
        )
        if SELECTED_DAY != dash.no_update:
            detail_refresh_required = True
        else:
            out_daily_status = "Invalid ID"

    # Refresh plot
    if plot_refresh_required:
        DATA_DAILY = daily_validation(
            station=STATION,
            variable=VARIABLE,
            start_time=START_DATE,
            end_time=END_DATE,
            minimum=MINIMUM,
            maximum=MAXIMUM,
        )
        out_plot = create_validation_plot(DATA_DAILY["series"])

        # Refresh daily table
        if daily_refresh_required:
            out_daily_row_data = DATA_DAILY["data"]
            if daily_reset_selection:
                out_daily_selected_rows = out_daily_row_data

    # Refresh detail table
    if detail_refresh_required:
        DATA_DETAIL = detail_list(
            station=STATION,
            variable=VARIABLE,
            date_of_interest=SELECTED_DAY,
            minimum=MINIMUM,
            maximum=MAXIMUM,
        )
        out_detail_row_data = DATA_DETAIL["series"]
        if detail_reset_selection:
            out_detail_selected_rows = out_detail_row_data

    return (
        out_daily_status,
        out_detail_status,
        out_plot,
        out_daily_row_data,
        out_detail_row_data,
        out_detail_row_transaction,
        out_detail_scroll,
        out_daily_selected_rows,
        out_detail_selected_rows,
    )
