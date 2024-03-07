import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html
from django_plotly_dash import DjangoDash

from measurement.models import Measurement, Report
from measurement.reporting import get_report_data_from_db
from station.models import Station
from variable.models import Variable

# Create a Dash app
app = DjangoDash(
    "DataReport",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)


# Initial values
init_station: str = Station.objects.order_by("station_code")[7].station_code
init_variable: str = Variable.objects.order_by("variable_code")[0].variable_code
init_start_time: str = "2023-03-01"
init_end_time: str = "2023-03-31"
init_temporality: str = "measurement"


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
            y=["average", "minimum", "maximum"],
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


plot = plot_graph(
    init_temporality,
    init_station,
    init_variable,
    init_start_time,
    init_end_time,
)


# Create layout
app.layout = html.Div(
    children=[
        html.Div(id="alert_div"),
        html.Div(
            style={"display": "flex", "justify-content": "space-around"},
            children=[
                html.Div(
                    style={"width": "35%"},
                    children=[
                        html.H2("Data Report"),
                        html.Button("Clear form", id="clear_button"),
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
                            value=init_temporality,
                        ),
                        html.H3("Station"),
                        dcc.Dropdown(
                            id="station_drop",
                            # options=Station.objects.order_by("station_code"),
                            options=[
                                item.station_code
                                for item in Station.objects.order_by("station_code")
                            ],
                            value=init_station,
                        ),
                        html.H3("Variable"),
                        dcc.Dropdown(
                            id="variable_drop",
                            options=[
                                {"label": item.name, "value": item.variable_code}
                                for item in Variable.objects.order_by("variable_code")
                            ],
                            value=init_variable,
                        ),
                        html.H3("Start date - End date"),
                        dcc.DatePickerRange(
                            id="date_range_picker",
                            display_format="YYYY-MM-DD",
                            start_date=init_start_time,
                            end_date=init_end_time,
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
        Output("temporality_drop", "value"),
        Output("station_drop", "value"),
        Output("variable_drop", "value"),
        Output("date_range_picker", "start_date"),
        Output("date_range_picker", "end_date"),
    ],
    Input("clear_button", "n_clicks"),
    prevent_initial_call=True,
)
def clear_form(n_clicks: int):
    return (
        init_temporality,
        init_station,
        init_variable,
        init_start_time,
        init_end_time,
    )


@app.callback(
    Output("alert_div", "children"),
    Input("data_report_graph", "figure"),
)
def invalid_data_alert(figure):
    if figure["layout"]["title"]["text"] == "Data not found":
        return [
            dbc.Alert("No data was found with the selected criteria", color="warning")
        ]
    else:
        return []
