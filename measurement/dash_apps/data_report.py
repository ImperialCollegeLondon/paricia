from logging import getLogger

import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash import Input, Output, State, dcc, html
from django_plotly_dash import DjangoDash

from variable.models import Variable

from ..filters import get_date_range, get_station_options, get_variable_options
from ..reporting import get_report_data_from_db
from .plots import create_empty_plot, create_report_plot

MAX_POINTS = 1000
"""Maximum number of points to display in the graph."""

# Create a Dash app
app = DjangoDash(
    "DataReport",
    external_stylesheets=[dbc.themes.BOOTSTRAP, "/static/styles/dashstyle.css"],
)

filters = html.Div(
    style={"width": "286px"},
    children=[
        html.Label("Temporality:", style={"font-weight": "bold"}),
        dcc.Dropdown(
            id="temporality_drop",
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
        html.Br(),
        html.Label("Station:", style={"font-weight": "bold"}),
        dcc.Dropdown(
            id="station_drop",
            options=[],
            value=None,
        ),
        html.Br(),
        html.Label("Variable:", style={"font-weight": "bold"}),
        dcc.Dropdown(
            id="variable_drop",
            options=[],
            value=None,
        ),
        html.Br(),
        html.Label("Date Range:", style={"font-weight": "bold"}),
        dcc.DatePickerRange(
            id="date_range_picker",
            display_format="YYYY-MM-DD",
            start_date=None,
            end_date=None,
        ),
        html.Br(),
        html.Div(
            id="csv_div",
            style={"margin-top": "30px"},
        ),
    ],
)

# Create layout
app.layout = html.Div(
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
                    style={"width": "65%"},
                    children=[
                        dcc.Graph(
                            id="data_report_graph",
                            figure=create_empty_plot(),
                        ),
                    ],
                ),
            ],
        ),
    ]
)


@app.callback(
    Output("data_report_graph", "figure"),
    [
        Input("data_report_graph", "relayoutData"),
        Input("display_button", "n_clicks"),
    ],
    [
        State("temporality_drop", "value"),
        State("station_drop", "value"),
        State("variable_drop", "value"),
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

        agg = ""
        if every > 1:
            aggregation = resampled["time"].diff().dt.seconds.mean() / 60
            unit = "minutes"
            if aggregation > 60:
                aggregation = aggregation / 60
                unit = "hours"
            if aggregation > 24:
                aggregation = aggregation / 24
                unit = "days"
            agg = f" - {aggregation:.1f} {unit} aggregation"

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
        State("temporality_drop", "value"),
        State("station_drop", "value"),
        State("variable_drop", "value"),
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
        Input("temporality_drop", "value"),
        Input("station_drop", "value"),
        Input("variable_drop", "value"),
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
        download = html.Button("Download CSV", id="csv_button")
        display = html.Button(
            "Display data",
            id="display_button",
            style={"margin-left": "10px"},
            n_clicks=0,
        )
        return [], [download, display]


@app.callback(
    [Output("station_drop", "options"), Output("station_drop", "value")],
    Input("stations_list", "children"),
)
def populate_stations_dropdown(
    station_codes: list[str],
) -> tuple[list[dict[str, str]], str | None]:
    """Populate the station dropdown based on the list of station codes."""
    return get_station_options(station_codes)


@app.callback(
    [Output("variable_drop", "options"), Output("variable_drop", "value")],
    Input("station_drop", "value"),
)
def populate_variable_dropdown(
    chosen_station: str,
) -> tuple[list[dict[str, str]], str | None]:
    """Populate the variable dropdown based on the chosen station."""
    return get_variable_options(chosen_station)


@app.callback(
    [
        Output("date_range_picker", "start_date"),
        Output("date_range_picker", "end_date"),
    ],
    [
        Input("station_drop", "value"),
        Input("variable_drop", "value"),
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
