# Formatting

The formatting application describes how a data file should be ingested: what columns to consider, what variable they contain, the format of date and time, etc. A summary of the models involved can be seen in the following diagram:

![UML diagram of the Formatting app models. Mandatory fields are in bold.](images/formatting.png)

## Basic components

::: formatting.models.Extension
    options:
      heading_level: 3
      show_bases: False
      members: None
      show_root_full_path: False

::: formatting.models.Delimiter
    options:
      heading_level: 3
      show_bases: False
      members: None
      show_root_full_path: False

::: formatting.models.Date
    options:
      heading_level: 3
      show_bases: False
      members: None
      show_root_full_path: False

::: formatting.models.Time
    options:
      heading_level: 3
      show_bases: False
      members: None
      show_root_full_path: False

## Core component

::: formatting.models.Format
    options:
      heading_level: 3
      show_bases: False
      members: None
      show_root_full_path: False

## Linking components

::: formatting.models.Association
    options:
      heading_level: 3
      show_bases: False
      members: None
      show_root_full_path: False

::: formatting.models.Classification
    options:
      heading_level: 3
      show_bases: False
      members: None
      show_root_full_path: False
