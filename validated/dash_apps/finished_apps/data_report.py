import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Input, Output, State, dcc, html
from django_plotly_dash import DjangoDash

from measurement.reporting import get_report_data_from_db
from validated.filters import get_date_range, get_station_options, get_variable_options
from variable.models import Variable

# Create a Dash app
app = DjangoDash(
    "DataReport",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)


def plot_graph(
    temporality: str,
    station: str,
    variable: str,
    start_time: str,
    end_time: str,
):
    # Load data
    try:
        data: pd.DataFrame = get_report_data_from_db(
            station=station,
            variable=variable,
            start_time=start_time,
            end_time=end_time,
            report_type=temporality,
        )

        variable_obj = Variable.objects.get(variable_code=variable)

        # Create plot
        plot = px.line(
            data,
            x="time",
            y=["value", "minimum", "maximum"],
            title=f"{station} - {variable_obj.name}",
        )

    except Exception as e:
        print("Error:", e)
        plot = px.line(title="Data not found")

    plot.update_layout(
        yaxis_title="",
        xaxis_title="",
    )

    return plot


plot = px.scatter()


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
                html.Div(
                    style={"width": "35%"},
                    children=[
                        html.H2("Data Report"),
                        html.H3("Temporality"),
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
                        html.H3("Station"),
                        dcc.Dropdown(
                            id="station_drop",
                            options=[],
                            value=None,
                        ),
                        html.H3("Variable"),
                        dcc.Dropdown(
                            id="variable_drop",
                            options=[],
                            value=None,
                        ),
                        html.H3("Start date - End date"),
                        dcc.DatePickerRange(
                            id="date_range_picker",
                            display_format="YYYY-MM-DD",
                            start_date=None,
                            end_date=None,
                        ),
                        html.Div(
                            id="csv_div",
                            style={"padding": "10px"},
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "65%"},
                    children=[
                        dcc.Graph(
                            id="data_report_graph",
                            figure=plot,
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
        Input("temporality_drop", "value"),
        Input("station_drop", "value"),
        Input("variable_drop", "value"),
        Input("date_range_picker", "start_date"),
        Input("date_range_picker", "end_date"),
    ],
)
def update_graph(
    temporality: str,
    station: str,
    variable: str,
    start_time: str,
    end_time: str,
) -> px.line:
    plot = plot_graph(
        temporality,
        station,
        variable,
        start_time,
        end_time,
    )

    return plot


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
                )
                .drop(columns=["station", "variable"])
                .to_csv(index=False)
            )
        except Exception as e:
            alert = dbc.Alert(f"Could not export data to CSV: {e}", color="warning")
            return None, [alert]
        return (
            dict(
                content=file,
                filename=f"{station}_{variable}_{temporality}_{start_time}-{end_time}.csv",
            ),
            [],
        )


@app.callback(
    [
        Output("data_alert_div", "children"),
        Output("csv_div", "children"),
    ],
    Input("data_report_graph", "figure"),
)
def update_alert(figure):
    if figure["layout"]["title"]["text"] == "Data not found":
        alert = dbc.Alert(
            "No data was found with the selected criteria", color="warning"
        )
        return [alert], []
    else:
        button = html.Button("Download CSV", id="csv_button")
        return [], [button]


@app.callback(
    [Output("station_drop", "options"), Output("station_drop", "value")],
    Input("stations_list", "children"),
)
def populate_stations_dropdown(station_codes: list[str]) -> tuple[list[dict], str]:
    """Populate the station dropdown based on the list of station codes."""
    return get_station_options(station_codes)


@app.callback(
    [Output("variable_drop", "options"), Output("variable_drop", "value")],
    Input("station_drop", "value"),
)
def populate_variable_dropdown(chosen_station: str) -> tuple[list[dict], str]:
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
) -> tuple[str, str,]:
    """Set the default date range based on the chosen station and variable."""
    return get_date_range(chosen_station, chosen_variable)
