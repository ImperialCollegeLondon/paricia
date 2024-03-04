import pandas as pd
import plotly.express as px


def create_validation_plot(
    data: pd.DataFrame, variable_name: str, field: str
) -> px.scatter:
    """Creates plot for Validation app

    Args:
        data (pd.DataFrame): Data
        variable_name (str): Variable name
        field (str): 'value', 'minimum' or 'maximum'

    Returns:
        px.Scatter: Plot
    """

    def status(row):
        if not row["is_validated"]:
            return "Unvalidated"
        if row["is_active"]:
            return "Active"
        return "Inactive"

    color_map = {
        "Active": "#00CC96",
        "Inactive": "#636EFA",
        "Unvalidated": "black",
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
            r=0,
            b=0,
            t=20,
        ),
    )

    return fig
