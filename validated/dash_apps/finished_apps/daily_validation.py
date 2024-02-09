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
from validated.plots import create_validation_plot
from validated.tables import create_columns_daily, create_columns_detail
from variable.models import Variable

DEFAULT_FONT = "Open Sans, Raleway, Dosis, Ubuntu, sans-serif"

app = DjangoDash("DailyValidation")

# Initial filters
STATION: Station = Station.objects.order_by("station_code")[7]
VARIABLE: Variable = Variable.objects.order_by("variable_code")[0]
START_DATE: datetime = datetime.strptime("2023-03-01", "%Y-%m-%d")
END_DATE: datetime = datetime.strptime("2023-03-31", "%Y-%m-%d")
MINIMUM: Decimal = Decimal(-5)
MAXIMUM: Decimal = Decimal(28)
SELECTED_DAY: datetime = datetime.strptime("2023-03-14", "%Y-%m-%d")
PLOT_TYPE = "average"

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

# Filters
filters = html.Div(
    children=[
        dcc.Dropdown(
            id="station_drop",
            options=[
                item.station_code for item in Station.objects.order_by("station_code")
            ],
            value=STATION.station_code,
        ),
        dcc.Dropdown(
            id="variable_drop",
            options=[
                {"label": item.name, "value": item.variable_code}
                for item in Variable.objects.order_by("variable_code")
            ],
            value=VARIABLE.variable_code,
        ),
        dcc.DatePickerRange(
            id="date_range_picker",
            display_format="YYYY-MM-DD",
            start_date=START_DATE.strftime("%Y-%m-%d"),
            end_date=END_DATE.strftime("%Y-%m-%d"),
        ),
        # dcc.Input(id="minimum_input", type="number", value=MINIMUM),
        # dcc.Input(id="maximum_input", type="number", value=MAXIMUM),
        html.Button("Submit", id="submit-button"),
    ]
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


# Date picker
detail_date_picker = html.Div(
    children=[
        html.Div(
            children=["Open detailed view"],
            style={
                "display": "inline-block",
                "font-family": DEFAULT_FONT,
                "padding-right": "5px",
                "font-size": "14px",
            },
        ),
        dcc.DatePickerSingle(
            id="detail-date-picker",
            display_format="YYYY-MM-DD",
            min_date_allowed=DATA_DAILY["data"][0]["date"],
            max_date_allowed=DATA_DAILY["data"][-1]["date"],
            style={"font-family": DEFAULT_FONT},
        ),
    ],
    style={"display": "inline-block", "width": "50%", "text-align": "right"},
)

# Table menu
menu = html.Div(
    children=[
        html.Div(
            children=[
                html.Button("Save to Validated", id="save-button"),
                html.Button("Reset Validated", id="reset-button"),
                html.Button("Add row", id="add-button", disabled=True),
            ],
            style={"display": "inline-block", "width": "50%"},
        ),
        detail_date_picker,
    ],
    style={
        "background-color": "#f0f0f0",
        "width": "100%",
    },
)

# Status message
status_message = html.Div(
    id="status-message",
    children=[""],
    style={
        "font-family": DEFAULT_FONT,
        "font-size": "14px",
        "min-height": "20px",
        "padding-top": "5px",
        "padding-bottom": "10px",
    },
)


# Plot
plot = create_validation_plot(data=DATA_DAILY, plot_type=PLOT_TYPE)

# Plot radio
plot_radio = dcc.RadioItems(
    id="plot_radio",
    options=[
        {"value": c, "label": c.capitalize()} for c in DATA_DAILY["value_columns"]
    ],
    value=PLOT_TYPE,
    inline=True,
    style={"font-family": DEFAULT_FONT, "font-size": "14px"},
)

# Layout
app.layout = html.Div(
    children=[
        filters,
        dcc.Tabs(
            id="tabs",
            value="tab-daily",
            style={"width": "100%"},
            children=[
                dcc.Tab(
                    label="Daily Report",
                    id="tab-daily",
                    value="tab-daily",
                    style={"font-family": DEFAULT_FONT},
                    selected_style={"font-family": DEFAULT_FONT},
                    children=[
                        table_daily,
                    ],
                ),
                dcc.Tab(
                    label="Detail of Selected Day",
                    id="tab-detail",
                    value="tab-detail",
                    disabled=True,
                    style={"font-family": DEFAULT_FONT},
                    selected_style={"font-family": DEFAULT_FONT},
                    disabled_style={"font-family": DEFAULT_FONT},
                    children=[
                        table_detail,
                    ],
                ),
            ],
        ),
        menu,
        status_message,
        dcc.Loading(
            type="dot",
            children=html.Div(id="loading"),
        ),
        plot_radio,
        dcc.Graph(id="plot", figure=plot, style={"width": "100%"}),
    ]
)


@app.callback(
    [
        Output("loading", "children"),
        Output("status-message", "children"),
        Output("plot", "figure"),
        Output("table_daily", "rowData"),
        Output("table_detail", "rowData"),
        Output("table_detail", "rowTransaction"),
        Output("table_detail", "scrollTo"),
        Output("table_daily", "selectedRows"),
        Output("table_detail", "selectedRows"),
        Output("tab-detail", "disabled"),
        Output("tab-detail", "label"),
        Output("tabs", "value"),
        Output("add-button", "disabled"),
    ],
    [
        Input("submit-button", "n_clicks"),
        Input("save-button", "n_clicks"),
        Input("reset-button", "n_clicks"),
        Input("add-button", "n_clicks"),
        Input("detail-date-picker", "date"),
        Input("plot_radio", "value"),
        Input("tabs", "value"),
    ],
    [
        State("station_drop", "value"),
        State("variable_drop", "value"),
        State("date_range_picker", "start_date"),
        State("date_range_picker", "end_date"),
        State("table_daily", "selectedRows"),
        State("table_daily", "rowData"),
        State("table_detail", "selectedRows"),
        State("table_detail", "rowData"),
    ],
    prevent_initial_call=True,
)
def callbacks(
    in_submit_clicks: int,
    in_save_clicks: int,
    in_reset_clicks: int,
    in_add_clicks: int,
    in_detail_date: datetime.date,
    in_plot_radio_value: str,
    in_tabs_value: str,
    in_station: str,
    in_variable: str,
    in_start_date: str,
    in_end_date: str,
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
    bool,
    str,
    str,
    bool,
]:
    """Callback for buttons adding and resetting Validated data

    Args:
        daily_save_clicks (int): Number of times daily-save-button was clicked
        daily_reset_clicks (int): Number of times daily-reset-button was clicked
        detail_save_clicks (int): Number of times detail-save-button was clicked
        detail_reset_clicks (int): Number of times detail-reset-button was clicked
        detail_add_clicks (int): Number of times detail-add-button was clicked
        daily_id (int): ID of selected day
        plot_radio_value (str): Value of plot radio button
        in_daily_selected_rows (list[dict]): Selected rows in table_daily
        in_detail_selected_rows (list[dict]): Selected rows in table_detail
        in_detail_row_data (list[dict]): Full row data for table_detail

    Returns:
        tuple[str, str, go.Figure, list[dict], list[dict], dict, dict, list[dict], list[dict], bool, str, str]:
            Callback outputs
    """
    global DATA_DAILY, DATA_DETAIL, STATION, VARIABLE, START_DATE, END_DATE, MINIMUM, MAXIMUM, SELECTED_DAY, PLOT_TYPE

    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]

    out_loading = dash.no_update
    out_status = dash.no_update
    out_plot = dash.no_update
    out_daily_row_data = dash.no_update
    out_detail_row_data = dash.no_update
    out_detail_row_transaction = dash.no_update
    out_detail_scroll = dash.no_update
    out_daily_selected_rows = dash.no_update
    out_detail_selected_rows = dash.no_update
    out_tab_detail_disabled = dash.no_update
    out_tab_detail_label = dash.no_update
    out_tabs_value = dash.no_update
    out_add_button_disabled = dash.no_update

    daily_data_refresh_required = False
    detail_data_refresh_required = False
    daily_table_refresh_required = False
    detail_table_refresh_required = False
    daily_table_reset_selection = False
    detail_table_reset_selection = False
    plot_refresh_required = False

    # Button: Submit
    if input_id == "submit-button":
        STATION = Station.objects.get(station_code=in_station)
        VARIABLE = Variable.objects.get(variable_code=in_variable)
        START_DATE = datetime.strptime(in_start_date, "%Y-%m-%d")
        END_DATE = datetime.strptime(in_end_date, "%Y-%m-%d")
        daily_data_refresh_required = True
        detail_data_refresh_required = True
        daily_table_refresh_required = True
        detail_table_refresh_required = True
        daily_table_reset_selection = True
        detail_table_reset_selection = True
        plot_refresh_required = True

    # Button: Save (daily)
    if input_id == "save-button" and in_tabs_value == "tab-daily":
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
        out_status = f"{len(in_daily_selected_rows)} days saved to Validated"
        daily_data_refresh_required = True
        daily_table_refresh_required = True
        plot_refresh_required = True

    # Button: Save (detail)
    elif input_id == "save-button" and in_tabs_value == "tab-detail":
        selected_ids = {row["id"] for row in in_detail_selected_rows}
        for row in in_detail_row_data:
            row["is_selected"] = row["id"] in selected_ids
        save_detail_to_validated(
            data_list=in_detail_row_data,
            variable=VARIABLE,
            station=STATION,
        )
        out_status = f"{len(in_detail_selected_rows)} entries saved to Validated"
        daily_data_refresh_required = True
        daily_table_refresh_required = True
        detail_data_refresh_required = True
        detail_table_refresh_required = True
        plot_refresh_required = True

    # Button: Reset (daily)
    elif input_id == "reset-button" and in_tabs_value == "tab-daily":
        reset_daily_validated(
            variable=VARIABLE,
            station=STATION,
            start_date=START_DATE,
            end_date=END_DATE,
        )
        out_status = "Validation reset"
        daily_data_refresh_required = True
        daily_table_refresh_required = True
        daily_table_reset_selection = True
        plot_refresh_required = True

    # Button: Reset (detail)
    elif input_id == "reset-button" and in_tabs_value == "tab-detail":
        reset_detail_validated(
            data_list=in_detail_row_data,
            variable=VARIABLE,
            station=STATION,
        )
        out_status = "Validation reset"
        daily_data_refresh_required = True
        daily_table_refresh_required = True
        detail_data_refresh_required = True
        detail_table_refresh_required = True
        detail_table_reset_selection = True
        plot_refresh_required = True

    # Button: New row (detail)
    elif input_id == "add-button" and in_tabs_value == "tab-detail":
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

    # Date picker
    elif input_id == "detail-date-picker":
        new_selected_day = next(
            (
                d["date"]
                for d in DATA_DAILY["data"]
                if d["date"].strftime("%Y-%m-%d") == in_detail_date
            ),
            None,
        )
        if new_selected_day is not None:
            SELECTED_DAY = new_selected_day
            detail_data_refresh_required = True
            detail_table_refresh_required = True
            detail_table_reset_selection = True
            out_tab_detail_disabled = False
            out_tab_detail_label = (
                f"Detail of Selected Day ({SELECTED_DAY.strftime('%Y-%m-%d')})"
            )
            out_tabs_value = "tab-detail"
            out_add_button_disabled = False
            out_status = ""
        else:
            out_status = "Invalid ID"

    # Plot radio
    elif input_id == "plot_radio":
        PLOT_TYPE = in_plot_radio_value
        plot_refresh_required = True

    # Switching tabs
    elif input_id == "tabs":
        if in_tabs_value == "tab-detail":
            out_add_button_disabled = False
        else:
            out_add_button_disabled = True

    # Reload daily data
    if daily_data_refresh_required:
        DATA_DAILY = daily_validation(
            station=STATION,
            variable=VARIABLE,
            start_time=START_DATE,
            end_time=END_DATE,
            minimum=MINIMUM,
            maximum=MAXIMUM,
        )

    # Reload detail data
    if detail_data_refresh_required:
        DATA_DETAIL = detail_list(
            station=STATION,
            variable=VARIABLE,
            date_of_interest=SELECTED_DAY,
            minimum=MINIMUM,
            maximum=MAXIMUM,
        )

    # Refresh plot
    if plot_refresh_required:
        out_plot = create_validation_plot(data=DATA_DAILY, plot_type=PLOT_TYPE)

    # Refresh daily table
    if daily_table_refresh_required:
        out_daily_row_data = DATA_DAILY["data"]

        # Reset daily table selection
        if daily_table_reset_selection:
            out_daily_selected_rows = out_daily_row_data

    # Refresh detail table
    if detail_table_refresh_required:
        out_detail_row_data = DATA_DETAIL["series"]

        # Reset detail table selection
        if detail_table_reset_selection:
            out_detail_selected_rows = out_detail_row_data

    return (
        out_loading,
        out_status,
        out_plot,
        out_daily_row_data,
        out_detail_row_data,
        out_detail_row_transaction,
        out_detail_scroll,
        out_daily_selected_rows,
        out_detail_selected_rows,
        out_tab_detail_disabled,
        out_tab_detail_label,
        out_tabs_value,
        out_add_button_disabled,
    )
