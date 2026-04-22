from logging import getLogger

import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash import Input, Output, State, dcc, html
from django_plotly_dash import DjangoDash

from variable.models import Variable

from ..filters import get_date_range, get_station_options, get_variable_options
from ..reporting import get_report_data_from_db
from .plots import (
    add_nans_for_gaps,
    create_empty_plot,
    create_report_plot,
    get_aggregation_level,
)

MAX_POINTS = 1000
"""Maximum number of points to display in the graph."""


def _traces_selection(block_id):
    """Build the traces selection widgets.

    Args:
        block_id (str): Prefix used to build the component id.

    Returns:
        html.Div: Scrollable container holding the traces selection widgets.
    """
    return html.Div(
        children=[
            html.Label("Temporality:", style={"font-weight": "bold"}),
            dcc.Dropdown(
                id=f"{block_id}_temporality_drop",
                options=[
                    {"label": "Raw measurement", "value": "measurement"},
                    {
                        "label": "Validated measurement",
                        "value": "validated",
                    },
                    {"label": "Hourly", "value": "hourly"},
                    {"label": "Daily", "value": "daily"},
                    {"label": "Monthly", "value": "monthly"},
                ],
                value="measurement",
            ),
            html.Label("Station:", style={"font-weight": "bold"}),
            dcc.Dropdown(
                id=f"{block_id}_station_drop",
                options=[],
                value=None,
            ),
            html.Label("Variable:", style={"font-weight": "bold"}),
            dcc.Dropdown(
                id=f"{block_id}_variable_drop",
                options=[],
                value=None,
            ),
        ],
    )


# Create a Dash app
app = DjangoDash(
    "DataReport",
    external_stylesheets=[dbc.themes.BOOTSTRAP, "/static/styles/dashstyle.css"],
)

secondary_trace = html.Div(
    style={"margin-top": "10px", "margin-left": "10px"},
    children=[
        dbc.Checklist(
            options=[
                {"label": "Add secondary trace", "value": 1},
            ],
            value=[],
            id="switch-show-secondary",
            switch=True,
        ),
        html.Div(
            _traces_selection("secondary"), id="secondary_traces_div", hidden=True
        ),
    ],
)

filters = html.Div(
    style={"width": "35%", "height": "100%", "padding": "10px"},
    children=[
        _traces_selection("primary"),
        html.Label("Date Range:", style={"font-weight": "bold"}),
        dcc.DatePickerRange(
            id="date_range_picker",
            display_format="YYYY-MM-DD",
            start_date=None,
            end_date=None,
        ),
        secondary_trace,
        html.Div(
            id="csv_div",
            style={"margin-top": "30px"},
        ),
    ],
)

# Create layout
app.layout = html.Div(
    style={"padding": "10px"},
    children=[
        html.Div(id="stations_list", hidden=True),
        dcc.Download(id="download_csv"),
        html.Div(
            id="data_alert_div",
            style={"padding": "10px"},
        ),
        html.Div(
            id="csv_alert_div",
            style={"padding": "10px"},
        ),
        html.Div(
            style={"display": "flex", "justify-content": "space-around"},
            children=[
                filters,
                html.Div(
                    style={"width": "100%", "height": "100%"},
                    children=[
                        dcc.Graph(
                            id="data_report_graph",
                            figure=create_empty_plot(),
                        ),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(
    Output("data_report_graph", "figure"),
    [
        Input("data_report_graph", "relayoutData"),
        Input("display_button", "n_clicks"),
    ],
    [
        State("primary_temporality_drop", "value"),
        State("primary_station_drop", "value"),
        State("primary_variable_drop", "value"),
        State("date_range_picker", "start_date"),
        State("date_range_picker", "end_date"),
        State("data_report_graph", "figure"),
    ],
)
def update_graph(
    relayout_data: dict,
    n_clicks: int,
    temporality: str,
    station: str,
    variable: str,
    start_time: str,
    end_time: str,
    figure: go.Figure,
    callback_context,
) -> go.Figure:
    ctx = callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else ""

    if not n_clicks:
        # After the first load, n_clicks is always > 0, so zooming works
        return figure

    # This is cached, so it's not a big deal to call it multiple times
    data = get_report_data_from_db(
        station=station,
        variable=variable,
        start_time=start_time,
        end_time=end_time,
        report_type=temporality,
        whole_months=False,
    )
    if data.empty:
        return create_empty_plot()

    if triggered_id == "data_report_graph" and "xaxis.range[0]" in relayout_data:
        start = relayout_data["xaxis.range[0]"]
        end = relayout_data["xaxis.range[1]"]
        data = data[(data["time"] >= start) & (data["time"] <= end)]

    try:
        every = max(1, len(data) // MAX_POINTS)
        resampled = data.iloc[::every]
        agg = get_aggregation_level(resampled["time"], every > 1)
        resampled = add_nans_for_gaps(resampled)

        plot = create_report_plot(
            data=resampled,
            variable_name=Variable.objects.get(variable_code=variable).name,
            station_code=station,
            agg=agg,
        )
        if "xaxis.range[0]" in relayout_data:
            plot["layout"]["xaxis"]["range"] = [
                relayout_data["xaxis.range[0]"],
                relayout_data["xaxis.range[1]"],
            ]
        return plot

    except Exception as e:
        getLogger().error(e)
        return create_empty_plot()


@app.callback(
    [
        Output("download_csv", "data"),
        Output("csv_alert_div", "children"),
    ],
    Input("csv_button", "n_clicks"),
    [
        State("primary_temporality_drop", "value"),
        State("primary_station_drop", "value"),
        State("primary_variable_drop", "value"),
        State("date_range_picker", "start_date"),
        State("date_range_picker", "end_date"),
    ],
    prevent_initial_call=True,
)
def download_csv_report(
    n_clicks: int,
    temporality: str,
    station: str,
    variable: str,
    start_time: str,
    end_time: str,
):
    if n_clicks and n_clicks > 0:
        try:
            file = (
                get_report_data_from_db(
                    station=station,
                    variable=variable,
                    start_time=start_time,
                    end_time=end_time,
                    report_type=temporality,
                    whole_months=False,
                )
                .drop(columns=["station", "variable", "data_import_id"])
                .dropna(axis=1, how="all")
                .dropna(axis=0)
                .to_csv(index=False)
            )
            return (
                dict(
                    content=file,
                    filename=f"{station}_{variable}_{temporality}_{start_time}-{end_time}.csv",
                ),
                [],
            )
        except Exception as e:
            alert = dbc.Alert(f"Could not export data to CSV: {e}", color="warning")
            return None, [alert]

    return None, []


@app.callback(
    [
        Output("data_alert_div", "children"),
        Output("csv_div", "children"),
    ],
    [
        Input("primary_temporality_drop", "value"),
        Input("primary_station_drop", "value"),
        Input("primary_variable_drop", "value"),
        Input("date_range_picker", "start_date"),
        Input("date_range_picker", "end_date"),
    ],
    State("data_report_graph", "figure"),
)
def update_alert(
    temporality: str,
    station: str,
    variable: str,
    start_time: str,
    end_time: str,
    figure: go.Figure,
):
    if figure["layout"]["title"]["text"] == "Data not found":
        alert = dbc.Alert(
            "No data was found with the selected criteria", color="warning"
        )
        return [alert], []
    else:
        download = dbc.Button(
            "Download CSV", color="primary", className="me-1", id="csv_button"
        )
        display = dbc.Button(
            "Display data",
            color="success",
            className="me-1",
            id="display_button",
            style={"margin-left": "10px"},
            n_clicks=0,
        )
        return [], [download, display]


@app.callback(
    Output("secondary_traces_div", "hidden"),
    Input("switch-show-secondary", "value"),
)
def toggle_secondary_traces_div(show_secondary: list[int]) -> bool:
    """Show or hide the secondary traces selection div based on the switch value."""
    return not bool(show_secondary)


@app.callback(
    [
        Output("primary_station_drop", "options"),
        Output("primary_station_drop", "value"),
        Output("secondary_station_drop", "options"),
        Output("secondary_station_drop", "value"),
    ],
    Input("stations_list", "children"),
)
def populate_stations_dropdown(
    station_codes: list[str],
) -> tuple[list[dict[str, str]], str | None, list[dict[str, str]], str | None]:
    """Populate the station dropdown based on the list of station codes."""
    options = get_station_options(station_codes)
    return *options, *options


@app.callback(
    [
        Output("primary_variable_drop", "options"),
        Output("primary_variable_drop", "value"),
        Output("secondary_variable_drop", "options"),
        Output("secondary_variable_drop", "value"),
    ],
    Input("primary_station_drop", "value"),
)
def populate_variable_dropdown(
    chosen_station: str,
) -> tuple[list[dict[str, str]], str | None, list[dict[str, str]], str | None]:
    """Populate the variable dropdown based on the chosen station."""
    options = get_variable_options(chosen_station)
    return *options, *options


@app.callback(
    [
        Output("date_range_picker", "start_date"),
        Output("date_range_picker", "end_date"),
    ],
    [
        Input("primary_station_drop", "value"),
        Input("primary_variable_drop", "value"),
    ],
)
def set_date_range(
    chosen_station, chosen_variable
) -> tuple[
    str,
    str,
]:
    """Set the default date range based on the chosen station and variable."""
    return get_date_range(chosen_station, chosen_variable)
