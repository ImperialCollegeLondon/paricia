from datetime import datetime

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


def get_aggregation_level(timeseries: pd.Series, aggregate: bool = False) -> str:
    """Calculates the aggregation level based on the timeseries separation.

    Args:
        timeseries: Time data to be aggregated.
        aggregate: Flag indicating if there should be aggregation

    Return:
        String indicating the aggregation level as " - LEVEL UNITS aggregation" or an
        empty string if no aggregation is required.
    """
    if not aggregate:
        return ""

    aggregation = timeseries.diff().dt.seconds.median() / 60
    unit = "minutes"
    if aggregation > 60:
        aggregation = aggregation / 60
        unit = "hours"
        if aggregation > 24:
            aggregation = aggregation / 24
            unit = "days"
    return f" - {aggregation:.1f} {unit} aggregation"


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
    data: pd.DataFrame,
    variable_name: str,
    station_code: str,
    agg: str = "",
) -> go.Figure:
    """Creates plot for Report app

    Args:
        data (pd.DataFrame): Data
        variable_name (str): Variable name
        station_code (str): Station code
        agg (str, optional): Aggregation level. Defaults to "".

    Returns:
        go.Figure: Plot
    """
    fig = go.Figure(
        [
            # Main trace
            go.Scatter(
                name=f"{variable_name}",
                x=data["time"],
                y=data["value"],
                mode="lines",
            ),
            # Maximum and minimum as filled area
            go.Scatter(
                name="Maximum",
                x=data["time"],
                y=data["maximum"],
                mode="lines",
                marker=dict(color="#444"),
                line=dict(width=0),
                showlegend=False,
            ),
            go.Scatter(
                name="Minimum",
                x=data["time"],
                y=data["minimum"],
                marker=dict(color="#444"),
                line=dict(width=0),
                mode="lines",
                fillcolor="rgba(68, 68, 68, 0.3)",
                fill="tonexty",
                showlegend=False,
            ),
        ]
    )

    fig.update_traces(marker=dict(size=3), connectgaps=False)
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


def add_nans_for_gaps(data: pd.DataFrame) -> pd.DataFrame:
    """Add NaN values to create gaps in the plot when there are missing points.

    Using values for maximum and minimum results in a shaded area indicating the gap
    which is more visually intuitive than just breaking the line.

    We use 1.5 times the median time difference as a threshold to detect gaps.

    Args:
        data: The data to process, must contain 'time', 'value', 'maximum' and 'minimum'
            columns.

    Returns:
        pd.DataFrame: Data with NaN values added for gaps
    """
    data = data.sort_values("time").reset_index(drop=True)
    data["time_diff"] = data["time"].diff()
    median_diff = data["time_diff"].median()
    gap_threshold = median_diff * 1.5
    gap_indices = data.index[data["time_diff"] > gap_threshold].tolist()
    data = data.drop(columns=["time_diff"])

    nan_rows: list[dict[str, float | datetime]] = []
    for idx in reversed(gap_indices):
        nan_rows.append(
            {
                "time": data.loc[idx, "time"] - median_diff / 2,
                "value": float("nan"),
                "maximum": data.loc[idx, "maximum"],
                "minimum": data.loc[idx, "minimum"],
            }
        )
    data = (
        pd.concat([data, pd.DataFrame(nan_rows)], ignore_index=True)
        .sort_values("time")
        .reset_index(drop=True)
    )

    return data
