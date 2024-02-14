import plotly.graph_objects as go


def create_validation_plot(data: dict, plot_type: str) -> go.Figure:
    """Creates plot for Validation app

    Args:
        data (dict): Daily data
        plot_type (str): Type of plot

    Returns:
        go.Figure: Plot
    """
    variable: str = data["variable"]["name"]
    data_series: dict = data["series"]
    is_cumulative: bool = data["variable"]["is_cumulative"]
    mode = "lines" if is_cumulative else "markers"

    fig = go.Figure()

    datasets = [
        {"key": "measurement", "name": "Measurement", "color": "black"},
        {"key": "selected", "name": "Selected", "color": "#636EFA"},
        {"key": "validated", "name": "Validated", "color": "#00CC96"},
    ]

    for dataset in datasets:
        fig.add_trace(
            go.Scatter(
                x=data_series[dataset["key"]]["time"],
                y=data_series[dataset["key"]][plot_type],
                name=dataset["name"],
                line=dict(color=dataset["color"]),
                mode=mode,
                marker_size=3,
            )
        )

    fig.update_yaxes(title_text=f"{variable} ({plot_type.capitalize()})")
    fig.update_layout(
        legend=dict(
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
