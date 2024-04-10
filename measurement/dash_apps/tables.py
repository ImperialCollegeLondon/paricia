"""
Functions defining columns and style conditions for tables in the measurement app

"""


def create_columns_daily() -> list:
    """Creates columns for Daily Report table

    Args:
        value_columns (list): List of value columns

    Returns:
        list: List of columns
    """
    styles = create_style_conditions()

    columns = [
        {
            "valueGetter": {
                "function": "d3.timeParse('%Y-%m-%d')(params.data.date.split('T')[0])"
            },
            "headerName": "Date",
            "filter": "agDateColumnFilter",
            "valueFormatter": {"function": "params.data.date.split('T')[0]"},
            "sort": "asc",
            **styles["date"],
        },
        *[
            {
                "field": c,
                "headerName": c.capitalize(),
                "filter": "agNumberColumnFilter",
                "valueFormatter": {"function": "d3.format(',.2f')(params.value)"},
                **styles[c],
            }
            for c in ["value", "minimum", "maximum"]
        ],
        {
            "field": "daily_count_fraction",
            "headerName": "Daily count fraction",
            "filter": "agNumberColumnFilter",
            "valueFormatter": {"function": "d3.format(',.2f')(params.value)"},
            **styles["daily_count_fraction"],
        },
        {
            "field": "total_suspicious_entries",
            "headerName": "Suspicious entries",
            "filter": "agNumberColumnFilter",
            **styles["total_suspicious_entries"],
        },
    ]
    return columns


def create_columns_detail() -> list:
    """Creates columns for Detail table

    Args:
        value_columns (list): List of value columns

    Returns:
        list: List of columns
    """
    styles = create_style_conditions()

    columns = [
        {
            "field": "id",
            "headerName": "Measurement ID",
            "filter": "agNumberColumnFilter",
        },
        {
            "field": "time",
            "valueFormatter": {"function": "params.value.split('T')[1].split('+')[0]"},
            "headerName": "Time",
            "editable": True,
            "sort": "asc",
            **styles["time"],
        },
        *[
            {
                "field": c,
                "headerName": c.capitalize(),
                "filter": "agNumberColumnFilter",
                "editable": True,
                "valueFormatter": {"function": "d3.format(',.2f')(params.value)"},
                **styles[c],
            }
            for c in ["value", "minimum", "maximum"]
        ],
    ]
    return columns


def create_style_condition(
    condition: str, style_true: dict, style_false: dict
) -> list[dict]:
    """Create a cell style condition

    Args:
        condition (str): Javascript code to evaluate
        style_true (dict): Style to apply when condition is true
        style_false (dict): Style to apply when condition is false

    Returns:
        list[dict]: Style condition
    """

    return [
        {
            "condition": condition,
            "style": style_true,
        },
        {
            "condition": f"!({condition})",
            "style": style_false,
        },
    ]


def create_style_conditions() -> dict:
    """Creates style conditions for Daily Report table

    Returns:
        dict: Style conditions
    """
    style_error = {"backgroundColor": "#E45756"}
    style_normal = {"backgroundColor": "transparent"}

    styles = {}

    styles["date"] = {
        "cellStyle": {
            "styleConditions": create_style_condition(
                condition="params.data['date_error'] > 0",
                style_true=style_error,
                style_false=style_normal,
            )
        },
    }

    styles["time"] = {
        "cellStyle": {
            "styleConditions": create_style_condition(
                condition="params.data['suspicious_time_lapse']",
                style_true=style_error,
                style_false=style_normal,
            )
        },
    }

    styles["value"] = {
        "cellStyle": {
            "styleConditions": create_style_condition(
                condition="params.data['suspicious_value_limits'] > 0 || params.data['suspicious_value_difference'] > 0",
                style_true=style_error,
                style_false=style_normal,
            )
        },
    }

    for field in ["maximum", "minimum"]:
        styles[field] = {
            "cellStyle": {
                "styleConditions": create_style_condition(
                    condition=f"params.data['suspicious_{field}_limits'] > 0",
                    style_true=style_error,
                    style_false=style_normal,
                )
            },
        }

    styles["daily_count_fraction"] = {
        "cellStyle": {
            "styleConditions": create_style_condition(
                condition="params.data['daily_count_fraction'] != 1",
                style_true=style_error,
                style_false=style_normal,
            )
        },
    }

    styles["total_suspicious_entries"] = {
        "cellStyle": {
            "styleConditions": create_style_condition(
                condition="params.data['total_suspicious_entries'] > 0",
                style_true=style_error,
                style_false=style_normal,
            )
        },
    }

    return styles
