"""
Functions defining columns and style conditions for tables in the validation app
  
"""


def create_columns_daily(value_columns: list) -> list:
    """Creates columns for Daily Report table

    Args:
        value_columns (list): List of value columns

    Returns:
        list: List of columns
    """
    styles = create_style_conditions_daily()

    columns = [
        {
            "field": "id",
            "headerName": "Id",
            "filter": "agNumberColumnFilter",
            "maxWidth": 150,
        },
        {
            "valueGetter": {"function": "d3.timeParse('%Y-%m-%d')(params.data.date)"},
            "headerName": "Date",
            "filter": "agDateColumnFilter",
            "valueFormatter": {"function": "params.data.date"},
            **styles["date"],
        },
        {
            "field": "percentage",
            "headerName": "Percnt.",
            "filter": "agNumberColumnFilter",
            **styles["percentage"],
        },
    ]

    additional_columns = [
        {
            "field": "sum",
            "headerName": "Sum",
            "filter": "agNumberColumnFilter",
            **styles["sum"],
        },
        {
            "field": "average",
            "headerName": "Average",
            "filter": "agNumberColumnFilter",
            **styles["average"],
        },
        {
            "field": "maximum",
            "headerName": "Max. of Maxs.",
            "filter": "agNumberColumnFilter",
            **styles["maximum"],
        },
        {
            "field": "minimum",
            "headerName": "Min. of Mins.",
            "filter": "agNumberColumnFilter",
            **styles["minimum"],
        },
    ]

    columns += [d for d in additional_columns if d["field"] in value_columns]

    columns += [
        {
            "field": "value_difference_error_count",
            "headerName": "Diff. Err",
            "filter": "agNumberColumnFilter",
            **styles["value_difference_error_count"],
        },
    ]
    return columns


def create_columns_detail(value_columns: list) -> list:
    """Creates columns for Detail table

    Args:
        value_columns (list): List of value columns

    Returns:
        list: List of columns
    """
    styles = create_style_conditions_detail(value_columns)

    columns = [
        {
            "field": "id",
            "headerName": "Id",
            "filter": "agNumberColumnFilter",
            "maxWidth": 150,
        },
        {
            "field": "time",
            "valueFormatter": {"function": "params.value.split('T')[1].split('+')[0]"},
            "headerName": "Time",
            "editable": True,
            **styles["time"],
        },
    ]
    columns += [
        {
            "field": c,
            "headerName": c[0].upper() + c[1:],
            "filter": "agNumberColumnFilter",
            "editable": True,
            **styles[c],
        }
        for c in value_columns
    ]
    columns += [
        {
            "field": "stddev_error",
            "headerName": "Outliers",
            "valueFormatter": {"function": "params.value ? 'X' : '-'"},
        },
        {"field": "value_difference", "headerName": "Value diff."},
    ]
    return columns


def create_style_conditions_daily() -> dict:
    """Creates style conditions for Daily Report table

    Returns:
        dict: Style conditions
    """
    styles = {}

    styles["id"] = {
        "cellStyle": {
            "styleConditions": [
                {
                    "condition": "params.data['all_validated']",
                    "style": {"backgroundColor": "#00CC96"},
                },
            ]
        },
    }

    styles["date"] = {
        "cellStyle": {
            "styleConditions": [
                {
                    "condition": "params.data['date_error'] > 0",
                    "style": {"backgroundColor": "#E45756"},
                },
            ]
        },
    }

    styles["percentage"] = {
        "cellStyle": {
            "styleConditions": [
                {
                    "condition": "params.data['percentage_error']",
                    "style": {"backgroundColor": "#E45756"},
                },
            ]
        },
    }

    styles["value_difference_error_count"] = {
        "cellStyle": {
            "styleConditions": [
                {
                    "condition": "params.data['value_difference_error_count'] > 0",
                    "style": {"backgroundColor": "#E45756"},
                },
            ]
        },
    }

    for field in ["sum", "average", "maximum", "minimum"]:
        styles[field] = {
            "cellStyle": {
                "styleConditions": [
                    {
                        "condition": f"params.data['suspicious_{field}s_count'] > 0",
                        "style": {"backgroundColor": "#E45756"},
                    },
                ]
            },
        }

    return styles


def create_style_conditions_detail(value_columns: list) -> dict:
    """Creates style conditions for Detail table

    Args:
        value_columns (list): List of value columns

    Returns:
        dict: Style conditions
    """
    styles = {}

    styles["time"] = {
        "cellStyle": {
            "styleConditions": [
                {
                    "condition": f"params.data['time_lapse_status'] == {val}",
                    "style": {"backgroundColor": f"{col}"},
                }
                for val, col in zip([0, 2], ["#E45756", "#FFA15A"])
            ]
        },
    }

    for field in value_columns + ["stdev", "value_difference"]:
        styles[field] = {
            "cellStyle": {
                "styleConditions": [
                    {
                        "condition": f"params.data['{field}_error']",
                        "style": {"backgroundColor": "#E45756"},
                    },
                ]
            },
        }

    return styles
