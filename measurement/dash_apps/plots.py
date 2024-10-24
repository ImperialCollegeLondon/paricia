import pandas as pd
import plotly.express as px
from plotly import graph_objs as go


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
    """Creates plot for Validation app

    Args:
        data (pd.DataFrame): Data
        variable_name (str): Variable name
        field (str): 'value', 'minimum' or 'maximum'

    Returns:
        go.Figure: Plot
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

    fig = px.scatter(
        data,
        x="time",
        y=field,
        color=data.apply(status, axis=1),
        color_discrete_map=color_map,
        labels={"time": "Date", field: f"{variable_name} ({field.capitalize()})"},
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
    """Creates plot for Report app

    Args:
        data (pd.DataFrame): Data
        variable_name (str): Variable name
        station_code (str): Station code

    Returns:
        go.Figure: Plot
    """

    fig = px.scatter(
        data,
        x="time",
        y=["value", "minimum", "maximum"],
        title=f"{station_code} - {variable_name}",
        labels={
            "time": "Date",
        },
    )

    fig.for_each_trace(
        lambda trace: trace.update(name=trace.name.title()),
    )
    fig.update_traces(marker=dict(size=3))
    fig.update_layout(
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
        yaxis_title=f"{variable_name}",
        title_font=dict(
            size=14,
        ),
    )

    return fig
