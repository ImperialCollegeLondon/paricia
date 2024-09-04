# Formatting

The formatting application describes how a data file should be ingested: what columns to consider, what variable they contain, the format of date and time, etc. A summary of the models involved can be seen in the following diagram:

![UML diagram of the Formatting app models. Mandatory fields are in bold.](images/formatting.png)

## Extension

This model contains the file extension of this type of data. It is mostly used to chose the tool to employed to ingest the data. While it can take any value, there is currently explicit support only for `xlsx` and `xlx`. Anything else will be interpreted as a text file and loaded using [`pandas.read_csv`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html).
