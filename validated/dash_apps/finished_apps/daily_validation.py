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
    dashGridOptions={
        "rowSelection": "multiple",
        "suppressRowClickSelection": True,
        "suppressScrollOnNewData": True,
    },
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
    dashGridOptions={
        "rowSelection": "multiple",
        "suppressRowClickSelection": True,
        "suppressScrollOnNewData": True,
    },
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
                mode="markers",
                marker_size=3,
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
        Output("table_daily", "selectedRows"),
        Output("table_detail", "selectedRows"),
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
def buttons_callback(
    daily_save_clicks: int,
    daily_reset_clicks: int,
    detail_save_clicks: int,
    detail_reset_clicks: int,
    in_daily_selected_rows: list[dict],
    in_detail_selected_rows: list[dict],
    in_detail_row_data: list[dict],
) -> tuple[str, str, go.Figure, list[dict], list[dict], list[dict], list[dict]]:
    """Callback for buttons adding and resetting Validated data

    Args:
        daily_save_clicks (int): Number of times daily-save-button was clicked
        daily_reset_clicks (int): Number of times daily-reset-button was clicked
        detail_save_clicks (int): Number of times detail-save-button was clicked
        detail_reset_clicks (int): Number of times detail-reset-button was clicked
        in_daily_selected_rows (list[dict]): Selected rows in table_daily
        in_detail_selected_rows (list[dict]): Selected rows in table_detail
        in_detail_row_data (list[dict]): Full row data for table_detail

    Returns:
        tuple[str, str, go.Figure, list[dict], list[dict], list[dict], list[dict]]:
            Callback outputs
    """

    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    out_daily_status = dash.no_update
    out_detail_status = dash.no_update
    out_plot = dash.no_update
    out_daily_row_data = dash.no_update
    out_detail_row_data = dash.no_update
    out_daily_selected_rows = dash.no_update
    out_detail_selected_rows = dash.no_update

    # Daily save
    if button_id == "daily-save-button" and in_daily_selected_rows is not None:
        conditions = get_conditions(in_daily_selected_rows)
        save_to_validated(
            variable=variable,
            station=station,
            to_delete=conditions,
            start_date=start_date,
            end_date=end_date,
            minimum=minimum,
            maximum=maximum,
        )
        out_daily_status = f"{len(in_daily_selected_rows)} days saved to Validated"

    # Daily reset
    elif button_id == "daily-reset-button":
        reset_daily_validated(
            variable=variable,
            station=station,
            start_date=start_date,
            end_date=end_date,
        )
        out_daily_status = "Validation reset"

    # Detail save
    elif button_id == "detail-save-button" and in_detail_selected_rows is not None:
        selected_ids = {row["id"] for row in in_detail_selected_rows}
        for row in in_detail_row_data:
            row["is_selected"] = row["id"] in selected_ids
        save_detail_to_validated(
            data_list=in_detail_row_data,
            variable=variable,
            station=station,
        )
        out_detail_status = f"{len(in_detail_selected_rows)} entries saved to Validated"

    # Detail reset
    elif button_id == "detail-reset-button":
        reset_detail_validated(
            data_list=in_detail_row_data,
            variable=variable,
            station=station,
        )
        out_detail_status = "Validation reset"

    # Reload daily data
    data_daily = daily_validation(
        station=station,
        variable=variable,
        start_time=start_date,
        end_time=end_date,
        minimum=minimum,
        maximum=maximum,
    )

    # Redraw plot
    out_plot = create_validation_plot(data_daily)

    # Reset tables
    if out_daily_status != dash.no_update:
        out_daily_row_data = data_daily["data"]
        daily_selected_ids = {row["id"] for row in in_daily_selected_rows}
        out_daily_selected_rows = [
            row for row in out_daily_row_data if row["id"] in daily_selected_ids
        ]
    elif out_detail_status != dash.no_update:
        data_detail = detail_list(
            station=station,
            variable=variable,
            date_of_interest=selected_day,
            minimum=minimum,
            maximum=maximum,
        )
        out_detail_row_data = data_detail["series"]
        detail_selected_ids = {row["id"] for row in in_detail_selected_rows}
        out_detail_selected_rows = [
            row for row in out_detail_row_data if row["id"] in detail_selected_ids
        ]

    return (
        out_daily_status,
        out_detail_status,
        out_plot,
        out_daily_row_data,
        out_detail_row_data,
        out_daily_selected_rows,
        out_detail_selected_rows,
    )


@app.callback(
    [Output("table_detail", "rowTransaction"), Output("table_detail", "scrollTo")],
    [Input("detail-add-button", "n_clicks")],
    [State("table_detail", "rowData")],
    prevent_initial_call=True,
)
def add_detail_row(detail_add_clicks: int, detail_row_data: list[dict]):
    # TODO: restore selection status
    # TODO: scroll to bottom
    last_id = detail_row_data[-1]["id"]
    last_time = detail_row_data[-1]["time"]
    new_row = {
        "id": last_id + 1,
        "time": last_time,
        **{key: None for key in data_daily["value_columns"]},
        "outlier": False,
        "value_difference": None,
        "is_selected": True,
    }
    return ({"add": [new_row]}, {"rowPosition": "bottom"})


@app.callback(
    [Output("table_detail", "scrollTo")],
    [Input("table_detail", "rowTransaction")],
    prevent_initial_call=True,
)
def scroll_to_bottom(row_transaction: dict):
    return ({"rowPosition": "bottom"},)
