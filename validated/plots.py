import pandas as pd
import plotly.express as px


def create_validation_plot(data: pd.DataFrame, variable: str, field: str) -> px.scatter:
    """Creates plot for Validation app

    Args:
        data (pd.DataFrame): Data
        variable (str): Variable name
        field (str): 'value', 'minimum' or 'maximum'

    Returns:
        px.Scatter: Plot
    """

    def status(row):
        if row["is_validated"]:
            return "Validated"
        if row["is_active"]:
            return "Active"
        return "Inactive"

    fig = px.scatter(
        data,
        x="time",
        y=field,
        color=data.apply(status, axis=1),
        labels={"time": "Date", field: f"{variable} ({field.capitalize()})"},
    )

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
