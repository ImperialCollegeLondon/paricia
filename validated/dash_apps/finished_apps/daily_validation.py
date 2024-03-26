from datetime import date
from decimal import Decimal

import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, State, dcc, html
from dash_ag_grid import AgGrid
from django_plotly_dash import DjangoDash

from measurement.models import Measurement, Station, Variable
from measurement.validation import (
    generate_validation_report,
    reset_validated_days,
    reset_validated_entries,
    save_validated_days,
    save_validated_entries,
)
from station.models import Station
from validated.plots import create_validation_plot
from validated.tables import create_columns_daily, create_columns_detail
from variable.models import Variable

app = DjangoDash(
    "DailyValidation", external_stylesheets=["/static/styles/dashstyle.css"]
)

# Initial filters
STATION: str = "CAR_02_HC_01"
VARIABLE: str = "airtemperature"
START_DATE: str = "2023-03-01"
END_DATE: str = "2023-03-31"
MINIMUM: Decimal = Decimal(-5)
MAXIMUM: Decimal = Decimal(28)
SELECTED_DAY: date = date(2023, 3, 14)
PLOT_FIELD = "value"

# Load initial data
DATA_SUMMARY, DATA_GRANULAR = generate_validation_report(
    station=STATION,
    variable=VARIABLE,
    start_time=START_DATE,
    end_time=END_DATE,
    minimum=MINIMUM,
    maximum=MAXIMUM,
    include_validated=True,
)

# Filters
filters = html.Div(
    children=[
        html.Div(
            [
                html.Label("Station:", style={"display": "block"}),
                dcc.Dropdown(
                    id="station_drop",
                    options=[
                        {"label": item.station_code, "value": item.station_code}
                        for item in Station.objects.order_by("station_code")
                    ],
                    value=STATION,
                ),
            ],
            style={"margin-right": "10px", "width": "250px"},
        ),
        html.Div(
            [
                html.Label("Variable:", style={"display": "block"}),
                dcc.Dropdown(
                    id="variable_drop",
                    options=[
                        {"label": item.name, "value": item.variable_code}
                        for item in Variable.objects.order_by("variable_code")
                    ],
                    value=VARIABLE,
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
                    start_date=START_DATE,
                    end_date=END_DATE,
                ),
            ],
            style={"margin-right": "10px", "width": "350px"},
        ),
        html.Div(
            [
                html.Label("Minimum:", style={"display": "block"}),
                dcc.Input(id="minimum_input", type="number", value=MINIMUM),
            ],
            style={"margin-right": "10px", "width": "200px"},
        ),
        html.Div(
            [
                html.Label("Maximum:", style={"display": "block"}),
                dcc.Input(id="maximum_input", type="number", value=MAXIMUM),
            ],
            style={"margin-right": "10px", "width": "200px"},
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
    rowData=DATA_GRANULAR[DATA_GRANULAR.time.dt.date == SELECTED_DAY].to_dict(
        "records"
    ),
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
            min_date_allowed=DATA_SUMMARY["date"].iloc[0].date(),
            max_date_allowed=DATA_SUMMARY["date"].iloc[-1].date(),
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
                html.Button("Reset Validation", id="reset-button"),
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
    value=PLOT_FIELD,
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
    ],
    [
        Input("submit-button", "n_clicks"),
        Input("save-button", "n_clicks"),
        Input("reset-button", "n_clicks"),
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
    ],
    prevent_initial_call=True,
)
def callbacks(
    in_submit_clicks: int,
    in_save_clicks: int,
    in_reset_clicks: int,
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
]:
    """Callbacks for daily validation app

    Args:
        in_submit_clicks (int): Number of times submit-button was clicked
        in_save_clicks (int): Number of times save-button was clicked
        in_reset_clicks (int): Number of times reset-button was clicked
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
        tuple[dash.no_update, dash.no_update, str, go.Figure, list[dict], list[dict], list[dict], list[dict], bool, str, str]: Outputs
    """
    global DATA_SUMMARY, DATA_GRANULAR, STATION, VARIABLE, START_DATE, END_DATE, MINIMUM, MAXIMUM, SELECTED_DAY, PLOT_FIELD

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

    data_refresh_required = False
    daily_table_refresh_required = False
    detail_table_refresh_required = False
    daily_table_reset_selection = False
    detail_table_reset_selection = False
    plot_refresh_required = False

    # Button: Submit
    if input_id == "submit-button":
        STATION = in_station
        VARIABLE = in_variable
        START_DATE = in_start_date
        END_DATE = in_end_date
        MINIMUM = Decimal(in_minimum) if in_minimum is not None else None
        MAXIMUM = Decimal(in_maximum) if in_maximum is not None else None
        out_status = ""
        data_refresh_required = True
        daily_table_refresh_required = True
        detail_table_refresh_required = True
        daily_table_reset_selection = True
        detail_table_reset_selection = True
        plot_refresh_required = True

    # Button: Save (daily)
    if input_id == "save-button" and in_tabs_value == "tab-daily":
        selected_dates = {row["date"] for row in in_daily_selected_rows}
        data_to_validate = [
            {
                "date": row["date"].split("T")[0],
                "validate?": True,
                "deactivate?": row["date"] not in selected_dates,
                "station": STATION,
                "variable": VARIABLE,
            }
            for row in in_daily_row_data
        ]
        save_validated_days(pd.DataFrame.from_records(data_to_validate))
        out_status = "Validation successful"
        data_refresh_required = True
        daily_table_refresh_required = True
        plot_refresh_required = True

    # Button: Save (detail)
    elif input_id == "save-button" and in_tabs_value == "tab-detail":
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
    elif input_id == "reset-button" and in_tabs_value == "tab-daily":
        reset_validated_days(
            variable=VARIABLE,
            station=STATION,
            start_date=START_DATE,
            end_date=END_DATE,
        )
        out_status = "Validation reset"
        data_refresh_required = True
        daily_table_refresh_required = True
        daily_table_reset_selection = True
        plot_refresh_required = True

    # Button: Reset (detail)
    elif input_id == "reset-button" and in_tabs_value == "tab-detail":
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
        PLOT_FIELD = in_plot_radio_value
        plot_refresh_required = True

    # Reload data
    if data_refresh_required:
        DATA_SUMMARY, DATA_GRANULAR = generate_validation_report(
            station=STATION,
            variable=VARIABLE,
            start_time=START_DATE,
            end_time=END_DATE,
            minimum=MINIMUM,
            maximum=MAXIMUM,
            include_validated=True,
        )

    # Refresh plot
    if plot_refresh_required:
        out_plot = create_validation_plot(
            data=DATA_GRANULAR,
            variable_name=Variable.objects.get(variable_code=VARIABLE).name,
            field=PLOT_FIELD,
        )

    # Refresh daily table
    if daily_table_refresh_required:
        out_daily_row_data = DATA_SUMMARY.to_dict("records")

        # Reset daily table selection
        if daily_table_reset_selection:
            out_daily_selected_rows = out_daily_row_data

    # Refresh detail table
    if detail_table_refresh_required:
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
    )


@app.callback(
    Output("station_drop", "options"),
    [Input("stations_list", "children"), Input("variable_drop", "value")],
)
def populate_stations_dropdown(station_codes, selected_variable):
    stations_for_variable = (
        Measurement.objects.filter(variable__variable_code=selected_variable)
        .values_list("station__station_code", flat=True)
        .distinct()
    )
    return [
        {"label": station_code, "value": station_code}
        for station_code in station_codes
        if station_code in stations_for_variable
    ]


@app.callback(Output("variable_drop", "options"), Input("station_drop", "value"))
def variable_dropdown(chosen_station):
    # Filter measurements based on the chosen station
    variable_dicts = (
        Measurement.objects.filter(station__station_code=chosen_station)
        .values("variable__name", "variable__variable_code")
        .distinct()
    )

    # Create a list of dictionaries for the dropdown
    return [
        {
            "label": variable["variable__name"],
            "value": variable["variable__variable_code"],
        }
        for variable in variable_dicts
    ]
