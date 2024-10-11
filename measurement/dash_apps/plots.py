import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly_resampler import FigureResampler


def create_empty_plot() -> px.scatter:
    """Creates empty plot

    Returns:
        px.Scatter: Plot
    """
    fig = px.scatter(title="No data to plot")
    fig.update_layout(
        autosize=True,
        margin=dict(
            l=50,
            r=20,
            b=0,
            t=50,
        ),
        title_font=dict(
            size=14,
        ),
    )
    return fig


def create_validation_plot(
    data: pd.DataFrame, variable_name: str, field: str
) -> go.Figure:
    """Creates plot for Validation app using plotly-resampler

    Args:
        data (pd.DataFrame): Data
        variable_name (str): Variable name
        field (str): 'value', 'minimum' or 'maximum'

    Returns:
        FigureResampler: Plot
    """

    def status(row):
        if not row["is_validated"]:
            return "Not validated"
        if row["is_active"]:
            return "Active"
        return "Inactive"

    color_map = {
        "Active": "#00CC96",
        "Inactive": "#636EFA",
        "Not validated": "black",
    }

    fig = FigureResampler(px.scatter)

    fig.add_trace(
        px.scatter(
            data,
            x="time",
            y=field,
            color=data.apply(status, axis=1),
            color_discrete_map=color_map,
            labels={"time": "Date", field: f"{variable_name} ({field.capitalize()})"},
        ).data[0]
    )

    fig.update_traces(marker=dict(size=3))
    fig.update_layout(
        legend=dict(
            title=dict(text="Status", font=dict(size=12)),
            x=1,
            y=1,
            xanchor="auto",
            yanchor="auto",
        ),
        autosize=True,
        margin=dict(
            l=50,
            r=20,
            b=0,
            t=50,
        ),
    )

    return fig


def create_report_plot(
    data: pd.DataFrame, variable_name: str, station_code: str
) -> go.Figure:
    """Creates plot for Report app using Plotly Resampler

    Args:
        data (pd.DataFrame): Data
        variable_name (str): Variable name
        station_code (str): Station code

    Returns:
        go.Figure: Plot
    """
    fig = FigureResampler(go.Figure())

    fig.add_trace(
        go.Scattergl(x=data["time"], y=data["value"], mode="markers", name="Value"),
        max_n_samples=1000,
        hf_marker_size=3.5,
    )
    fig.add_trace(
        go.Scattergl(x=data["time"], y=data["minimum"], mode="markers", name="Minimum"),
        max_n_samples=1000,
        hf_marker_size=3.5,
    )
    fig.add_trace(
        go.Scattergl(x=data["time"], y=data["maximum"], mode="markers", name="Maximum"),
        max_n_samples=1000,
        hf_marker_size=3.5,
    )

    fig.update_layout(
        title=f"{station_code} - {variable_name}",
        xaxis_title="Date",
        yaxis_title=f"{variable_name}",
        legend=dict(
            title=dict(text="", font=dict(size=12)),
            x=1,
            y=1,
            xanchor="auto",
            yanchor="auto",
        ),
        autosize=True,
        margin=dict(
            l=50,
            r=20,
            b=0,
            t=50,
        ),
        title_font=dict(
            size=14,
        ),
    )

    return fig
