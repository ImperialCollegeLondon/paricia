from datetime import date
from decimal import Decimal

import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, State, dcc, html
from dash_ag_grid import AgGrid
from django_plotly_dash import DjangoDash

from measurement.validation import (
    generate_validation_report,
    reset_validated_days,
    reset_validated_entries,
    save_validated_days,
    save_validated_entries,
)
from validated.filters import (
    populate_stations_dropdown_util,
    populate_variable_dropdown_util,
    set_date_range_util,
    set_min_max_util,
)
from validated.plots import create_validation_plot
from validated.tables import create_columns_daily, create_columns_detail
from variable.models import Variable

app = DjangoDash(
    "DailyValidation", external_stylesheets=["/static/styles/dashstyle.css"]
)

# Globals
SELECTED_DAY: date = None
DATA_SUMMARY: pd.DataFrame = None
DATA_GRANULAR: pd.DataFrame = None

# Filters
filters = html.Div(
    children=[
        html.Div(
            [
                html.Label("Station:", style={"display": "block"}),
                dcc.Dropdown(
                    id="station_drop",
                    options=[],
                    value=None,
                ),
            ],
            style={"margin-right": "10px", "width": "250px"},
        ),
        html.Div(
            [
                html.Label("Variable:", style={"display": "block"}),
                dcc.Dropdown(
                    id="variable_drop",
                    options=[],
                    value=None,
                ),
            ],
            style={"margin-right": "10px", "width": "250px"},
        ),
        html.Div(
            [
                html.Label("Date Range:", style={"display": "block"}),
                dcc.DatePickerRange(
                    id="date_range_picker",
                    display_format="YYYY-MM-DD",
                    start_date=None,
                    end_date=None,
                ),
            ],
            style={"margin-right": "10px", "width": "350px"},
        ),
        html.Div(
            [
                html.Label("Minimum:", style={"display": "block"}),
                dcc.Input(id="minimum_input", type="number", value=None),
            ],
            style={"margin-right": "10px", "width": "200px"},
        ),
        html.Div(
            [
                html.Label("Maximum:", style={"display": "block"}),
                dcc.Input(id="maximum_input", type="number", value=None),
            ],
            style={"margin-right": "10px", "width": "200px"},
        ),
        html.Div(
            [
                html.Label("Validation status:", style={"display": "block"}),
                dcc.Dropdown(
                    id="validation_status_drop",
                    options=[
                        {"label": "Validated", "value": "validated"},
                        {"label": "Not validated", "value": "not_validated"},
                    ],
                    value="not_validated",
                ),
            ],
            style={"width": "200px"},
        ),
    ],
    style={
        "display": "flex",
        "justify-content": "flex-start",
        "font-size": "14px",
    },
)

# Tables
table_daily = AgGrid(
    id="table_daily",
    rowData=[],
    columnDefs=create_columns_daily(),
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
    getRowId="params.data.date",
)

table_detail = AgGrid(
    id="table_detail",
    rowData=[],
    columnDefs=create_columns_detail(),
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
                "padding-right": "5px",
                "font-size": "14px",
            },
        ),
        dcc.DatePickerSingle(
            id="detail-date-picker",
            display_format="YYYY-MM-DD",
            min_date_allowed=None,
            max_date_allowed=None,
        ),
    ],
    style={
        "display": "inline-block",
        "width": "50%",
        "text-align": "right",
    },
)

# Table menu
menu = html.Div(
    children=[
        html.Div(
            children=[
                html.Button("Validate", id="save-button"),
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
        "font-size": "14px",
        "min-height": "20px",
        "padding-top": "5px",
        "padding-bottom": "10px",
    },
)


# Plot
plot = px.scatter()

# Plot radio
plot_radio = dcc.RadioItems(
    id="plot_radio",
    options=[
        {"value": c, "label": c.capitalize()} for c in ["value", "maximum", "minimum"]
    ],
    value="value",
    inline=True,
    style={"font-size": "14px"},
)

# Layout
app.layout = html.Div(
    children=[
        html.Div(id="stations_list", hidden=True),
        filters,
        html.Button("Submit", id="submit-button", style={"margin-top": "10px"}),
        dcc.Loading(
            type="dot",
            children=html.Div(id="loading_top"),
        ),
        html.Hr(),
        dcc.Tabs(
            id="tabs",
            value="tab-daily",
            style={"width": "100%"},
            children=[
                dcc.Tab(
                    label="Daily Report",
                    id="tab-daily",
                    value="tab-daily",
                    children=[
                        table_daily,
                    ],
                ),
                dcc.Tab(
                    label="Detail of Selected Day",
                    id="tab-detail",
                    value="tab-detail",
                    disabled=True,
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
        html.Hr(),
        plot_radio,
        dcc.Graph(id="plot", figure=plot, style={"width": "100%"}),
    ]
)


@app.callback(
    [
        Output("loading_top", "children"),
        Output("loading", "children"),
        Output("status-message", "children"),
        Output("plot", "figure"),
        Output("table_daily", "rowData"),
        Output("table_detail", "rowData"),
        Output("table_daily", "selectedRows"),
        Output("table_detail", "selectedRows"),
        Output("tab-detail", "disabled"),
        Output("tab-detail", "label"),
        Output("tabs", "value"),
        Output("save-button", "children"),
    ],
    [
        Input("submit-button", "n_clicks"),
        Input("save-button", "n_clicks"),
        Input("detail-date-picker", "date"),
        Input("plot_radio", "value"),
    ],
    [
        State("tabs", "value"),
        State("station_drop", "value"),
        State("variable_drop", "value"),
        State("date_range_picker", "start_date"),
        State("date_range_picker", "end_date"),
        State("minimum_input", "value"),
        State("maximum_input", "value"),
        State("table_daily", "selectedRows"),
        State("table_daily", "rowData"),
        State("table_detail", "selectedRows"),
        State("table_detail", "rowData"),
        State("validation_status_drop", "value"),
    ],
    prevent_initial_call=True,
)
def callbacks(
    in_submit_clicks: int,
    in_save_clicks: int,
    in_detail_date: str,
    in_plot_radio_value: str,
    in_tabs_value: str,
    in_station: str,
    in_variable: str,
    in_start_date: str,
    in_end_date: str,
    in_minimum: float,
    in_maximum: float,
    in_daily_selected_rows: list[dict],
    in_daily_row_data: list[dict],
    in_detail_selected_rows: list[dict],
    in_detail_row_data: list[dict],
    in_validation_status: str,
) -> tuple[
    dash.no_update,
    dash.no_update,
    str,
    go.Figure,
    list[dict],
    list[dict],
    list[dict],
    list[dict],
    bool,
    str,
    str,
    str,
]:
    """Callbacks for daily validation app

    Args:
        in_submit_clicks (int): Number of times submit-button was clicked
        in_save_clicks (int): Number of times save-button was clicked
        in_detail_date (str): Date for detail view
        in_plot_radio_value (str): Value of plot radio button
        in_tabs_value (str): Value of tabs
        in_station (str): Station from filters
        in_variable (str): Variable from filters
        in_start_date (str): Start date from filters
        in_end_date (str): End date from filters
        in_minimum (float): Minimum from filters
        in_maximum (float): Maximum from filters
        in_daily_selected_rows (list[dict]): Selected rows in table_daily
        in_daily_row_data (list[dict]): Full row data for table_daily
        in_detail_selected_rows (list[dict]): Selected rows in table_detail
        in_detail_row_data (list[dict]): Full row data for table_detail

    Returns:
        out_loading_top (dash.no_update): Loading spinner for top
        out_loading (dash.no_update): Loading spinner for bottom
        out_status (str): Status message
        out_plot (go.Figure): Plot
        out_daily_row_data (list[dict]): Data for daily table
        out_detail_row_data (list[dict]): Data for detail table
        out_daily_selected_rows (list[dict]): Selected rows in daily table
        out_detail_selected_rows (list[dict]): Selected rows in detail table
        out_tab_detail_disabled (bool): Disabled status for detail tab
        out_tab_detail_label (str): Label for detail tab
        out_tabs_value (str): Value for tabs
        out_save_label (str): Label for save button
    """
    global SELECTED_DAY, DATA_SUMMARY, DATA_GRANULAR

    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]

    out_loading_top = dash.no_update
    out_loading = dash.no_update
    out_status = dash.no_update
    out_plot = dash.no_update
    out_daily_row_data = dash.no_update
    out_detail_row_data = dash.no_update
    out_daily_selected_rows = dash.no_update
    out_detail_selected_rows = dash.no_update
    out_tab_detail_disabled = dash.no_update
    out_tab_detail_label = dash.no_update
    out_tabs_value = dash.no_update
    out_save_label = dash.no_update

    data_refresh_required = False
    daily_table_refresh_required = False
    detail_table_refresh_required = False
    daily_table_reset_selection = False
    detail_table_reset_selection = False
    plot_refresh_required = False

    # Button: Submit
    if input_id == "submit-button":
        out_status = ""
        out_save_label = (
            "Validate"
            if in_validation_status == "not_validated"
            else "Reset Validation"
        )
        data_refresh_required = True
        daily_table_refresh_required = True
        detail_table_refresh_required = True
        daily_table_reset_selection = True
        detail_table_reset_selection = True
        plot_refresh_required = True

    # Button: Save (daily)
    if (
        input_id == "save-button"
        and in_tabs_value == "tab-daily"
        and in_validation_status == "not_validated"
    ):
        selected_dates = {row["date"] for row in in_daily_selected_rows}
        data_to_validate = [
            {
                "date": row["date"].split("T")[0],
                "validate?": True,
                "deactivate?": row["date"] not in selected_dates,
                "station": in_station,
                "variable": in_variable,
            }
            for row in in_daily_row_data
        ]
        save_validated_days(pd.DataFrame.from_records(data_to_validate))
        out_status = "Validation successful"
        data_refresh_required = True
        daily_table_refresh_required = True
        plot_refresh_required = True

    # Button: Save (detail)
    elif (
        input_id == "save-button"
        and in_tabs_value == "tab-detail"
        and in_validation_status == "not_validated"
    ):
        selected_ids = {row["id"] for row in in_detail_selected_rows}
        data_to_validate = [
            {
                "id": row["id"],
                "validate?": True,
                "deactivate?": row["id"] not in selected_ids,
                "value": row["value"],
                "minimum": row["minimum"],
                "maximum": row["maximum"],
            }
            for row in in_detail_row_data
        ]
        save_validated_entries(pd.DataFrame.from_records(data_to_validate))
        out_status = "Validation successful"
        data_refresh_required = True
        daily_table_refresh_required = True
        detail_table_refresh_required = True
        plot_refresh_required = True

    # Button: Reset (daily)
    elif (
        input_id == "save-button"
        and in_tabs_value == "tab-daily"
        and in_validation_status == "validated"
    ):
        reset_validated_days(
            variable=in_variable,
            station=in_station,
            start_date=in_start_date,
            end_date=in_end_date,
        )
        out_status = "Validation reset"
        data_refresh_required = True
        daily_table_refresh_required = True
        daily_table_reset_selection = True
        plot_refresh_required = True

    # Button: Reset (detail)
    elif (
        input_id == "save-button"
        and in_tabs_value == "tab-detail"
        and in_validation_status == "validated"
    ):
        reset_validated_entries(ids=[row["id"] for row in in_detail_row_data])
        out_status = "Validation reset"
        data_refresh_required = True
        daily_table_refresh_required = True
        detail_table_refresh_required = True
        detail_table_reset_selection = True
        plot_refresh_required = True

    # Date picker
    elif input_id == "detail-date-picker":
        new_selected_day = next(
            (
                d.date()
                for d in DATA_SUMMARY["date"]
                if d.strftime("%Y-%m-%d") == in_detail_date
            ),
            None,
        )
        if new_selected_day is not None:
            SELECTED_DAY = new_selected_day
            detail_table_refresh_required = True
            detail_table_reset_selection = True
            out_tab_detail_disabled = False
            out_tab_detail_label = (
                f"Detail of Selected Day ({SELECTED_DAY.strftime('%Y-%m-%d')})"
            )
            out_tabs_value = "tab-detail"
            out_status = ""
        else:
            out_status = "No data for selected day"

    # Plot radio
    elif input_id == "plot_radio":
        plot_refresh_required = True

    # Reload data
    if data_refresh_required:
        DATA_SUMMARY, DATA_GRANULAR = generate_validation_report(
            station=in_station,
            variable=in_variable,
            start_time=in_start_date,
            end_time=in_end_date,
            minimum=Decimal(in_minimum) if in_minimum is not None else None,
            maximum=Decimal(in_maximum) if in_maximum is not None else None,
            include_validated=in_validation_status == "validated",
            only_validated=in_validation_status == "validated",
        )
        if DATA_SUMMARY.empty:
            out_status = "No data available"

    # Refresh plot
    if plot_refresh_required:
        if not DATA_GRANULAR.empty:
            out_plot = create_validation_plot(
                data=DATA_GRANULAR,
                variable_name=Variable.objects.get(variable_code=in_variable).name,
                field=in_plot_radio_value,
            )
        else:
            out_plot = px.scatter()

    # Refresh daily table
    if daily_table_refresh_required:
        out_daily_row_data = DATA_SUMMARY.to_dict("records")

        # Reset daily table selection
        if daily_table_reset_selection:
            out_daily_selected_rows = out_daily_row_data

    # Refresh detail table
    if detail_table_refresh_required and not DATA_GRANULAR.empty:
        out_detail_row_data = DATA_GRANULAR[
            DATA_GRANULAR.time.dt.date == SELECTED_DAY
        ].to_dict("records")

        # Reset detail table selection
        if detail_table_reset_selection:
            out_detail_selected_rows = out_detail_row_data

    return (
        out_loading_top,
        out_loading,
        out_status,
        out_plot,
        out_daily_row_data,
        out_detail_row_data,
        out_daily_selected_rows,
        out_detail_selected_rows,
        out_tab_detail_disabled,
        out_tab_detail_label,
        out_tabs_value,
        out_save_label,
    )


@app.callback(
    [Output("station_drop", "options"), Output("station_drop", "value")],
    Input("stations_list", "children"),
)
def populate_stations_dropdown(station_codes: list[str]) -> tuple[list[dict], str]:
    """Populate the station dropdown based on the list of station codes."""
    return populate_stations_dropdown_util(station_codes)


@app.callback(
    [Output("variable_drop", "options"), Output("variable_drop", "value")],
    Input("station_drop", "value"),
)
def populate_variable_dropdown(chosen_station: str) -> tuple[list[dict], str]:
    """Populate the variable dropdown based on the chosen station."""
    return populate_variable_dropdown_util(chosen_station)


@app.callback(
    [
        Output("date_range_picker", "start_date"),
        Output("date_range_picker", "end_date"),
        Output("minimum_input", "value"),
        Output("maximum_input", "value"),
    ],
    [
        Input("station_drop", "value"),
        Input("variable_drop", "value"),
    ],
)
def set_date_range_min_max(
    chosen_station, chosen_variable
) -> tuple[str, str, Decimal, Decimal,]:
    """Set the default date range and min/max based on the chosen station and
    variable."""
    start_date, end_date = set_date_range_util(chosen_station, chosen_variable)
    min_val, max_val = set_min_max_util(chosen_station, chosen_variable)
    return start_date, end_date, min_val, max_val


@app.callback(
    Output("detail-date-picker", "min_date_allowed"),
    Output("detail-date-picker", "max_date_allowed"),
    Input("table_daily", "rowData"),
    prevent_initial_call=True,
)
def set_detail_date_range(daily_row_data) -> tuple[str, str]:
    """Set the min and max date for the detail date picker based on the daily data.

    This will run whenever the data is updated.

    Args:
        daily_row_data (list[dict]): Data for the daily table

    Returns:
        tuple[str, str]: Min date, max date
    """
    min_date = min(daily_row_data, key=lambda x: x["date"])["date"]
    max_date = max(daily_row_data, key=lambda x: x["date"])["date"]
    return min_date, max_date
