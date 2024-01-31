from dash_ag_grid import AgGrid


def get_columns_daily(value_columns):
    styles = get_daily_style_data_conditional()

    columns = [
        {
            "field": "id",
            "headerName": "Id",
            "filter": "agNumberColumnFilter",
        },
        {
            "field": "date",
            "headerName": "Date",
            "filter": "agDateColumnFilter",
            **styles["date"],
        },
        {
            "field": "percentage",
            "headerName": "Percnt.",
            "filter": "agNumberColumnFilter",
            **styles["percentage"],
        },
        {
            "field": "value_difference_error_count",
            "headerName": "Diff. Err",
            "filter": "agNumberColumnFilter",
            **styles["value_difference_error_count"],
        },
    ]

    optional_columns = [
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

    columns += [d for d in optional_columns if d["field"] in value_columns]
    return columns


def get_columns_detail(value_columns):
    styles = get_detail_style_data_conditional(value_columns)

    columns = [
        {"field": "id", "headerName": "Id", "filter": "agNumberColumnFilter"},
        {
            "field": "time",
            "headerName": "Time",
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
        {"field": "stdev_error", "headerName": "Outliers"},
        {"field": "value_difference", "headerName": "Value diff."},
    ]
    return columns


def get_daily_style_data_conditional():
    styles = {}

    styles["date"] = {
        "cellStyle": {
            "styleConditions": [
                {
                    "condition": "params.data['date_error'] > 0",
                    "style": {"backgroundColor": "sandybrown"},
                },
            ]
        },
    }

    styles["percentage"] = {
        "cellStyle": {
            "styleConditions": [
                {
                    "condition": "params.data['percentage_error']",
                    "style": {"backgroundColor": "sandybrown"},
                },
            ]
        },
    }

    styles["value_difference_error_count"] = {
        "cellStyle": {
            "styleConditions": [
                {
                    "condition": "params.data['value_difference_error_count'] > 0",
                    "style": {"backgroundColor": "sandybrown"},
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
                        "style": {"backgroundColor": "sandybrown"},
                    },
                ]
            },
        }

    return styles


def get_detail_style_data_conditional(value_columns):
    styles = {}

    styles["time"] = {
        "cellStyle": {
            "styleConditions": [
                {
                    "condition": f"params.data['time_lapse_status'] == {val}",
                    "style": {"backgroundColor": f"{col}"},
                }
                for val, col in zip([0, 2], ["sandybrown", "yellow"])
            ]
        },
    }

    for field in value_columns + ["stdev", "value_difference"]:
        styles[field] = {
            "cellStyle": {
                "styleConditions": [
                    {
                        "condition": f"params.data['{field}_error']",
                        "style": {"backgroundColor": "sandybrown"},
                    },
                ]
            },
        }

    return styles


def create_daily_table(data):
    table = AgGrid(
        id="table",
        rowData=data["data"],
        columnDefs=get_columns_daily(value_columns=data["value_columns"]),
        columnSize="sizeToFit",
        defaultColDef={
            "resizable": False,
            "sortable": True,
            "checkboxSelection": {
                "function": "params.column == params.columnApi.getAllDisplayedColumns()[0]"
            },
            "headerCheckboxSelection": {
                "function": "params.column == params.columnApi.getAllDisplayedColumns()[0]"
            },
            "headerCheckboxSelectionFilteredOnly": True,
        },
        dashGridOptions={"rowSelection": "multiple", "suppressRowClickSelection": True},
        selectAll=True,
    )
    return table


def create_detail_table(data_detail):
    table = AgGrid(
        id="table_detail",
        rowData=data_detail["series"],
        columnDefs=get_columns_detail(value_columns=data_detail["value_columns"]),
        columnSize="sizeToFit",
        defaultColDef={
            "resizable": False,
            "sortable": True,
            "checkboxSelection": {
                "function": "params.column == params.columnApi.getAllDisplayedColumns()[0]"
            },
            "headerCheckboxSelection": {
                "function": "params.column == params.columnApi.getAllDisplayedColumns()[0]"
            },
            "headerCheckboxSelectionFilteredOnly": True,
        },
        dashGridOptions={"rowSelection": "multiple", "suppressRowClickSelection": True},
        selectAll=True,
    )
    return table
