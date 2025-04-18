# Validation

Validation is the process by which data ingested by the database is reviewed by an operator and either discarded, amended or accepted - and therefore used to create reports.

## Selecting the data to validate

The process starts by selecting the data to be validated in the validation page. **Only registered users with change permissions for a particular station can validate data for that station**. Once the station is selected, the variables available for that station are displayed, as well as other filters based on their values, date range or status. By default, all non-validated data for the selected variable and station is displayed once the `Submit` button is clicked.

![Selection of the data to validate](assets/images/validation_selector.png)

!!! tip "Minimise the date range"

    While the database can handle queries of millions of entries at once, such data will need to be manipulated, pre-analysed for suspicious values and then sent from the server to the browser and included in the table and the plot underneath. Therefore, it is important that users choose just the date range they are interested in exploring to minimise the loading times and make the whole process more fluid.

## The daily report

After submitting the data request, a table with a daily report is displayed, as well as a plot underneath. Both are useful to identify suspicious entries in the data that should be either manually fixed or discarded.

For example, the following image shows that there is a problem in first day, 2023-03-14, by highlighting in red the problematic cell. In particular, it shows that, based on the expected time difference between data points (taken as the mode of the time difference for all the data in the range), there is only 80% of the data expected for this day. In addition, there are 2 suspicious entries on that day.

![Daily report showing some suspicious entries](assets/images/validation_table.png)

If we scroll down in the table, we can see that there are more problems with this data. The last day only has 21% of the expected data, two suspicious entries and a problem with the `value` field. The second to last is even worse, with twice as many entries as it should and over 303 of them suspicious. The plot underneath also points to a potential problem - a gap in the data series.

![Daily report with more suspicious entries and the plot](assets/images/validation_table_other_errors.png)

## The detail for the day

To find out exactly what the suspicious entries are about, we can select the specific day in the date selector of the bottom-right corner. The entries for the selected day will be displayed in another tab within the same table.

We can find the suspicious entries, 2 in the first case, by scrolling the table in search of flagged cells. We can see that two entries are flagged together, in the time column. This indicates a problem with the timing of these entries. It can be seen that the issue is that the periodicity is not correct, with a separation of 2 and 3 minutes with respect to the previous point, while that separation should be 5 min according to the station metadata. Most likely, the point in line 95 should not be there.

![Exploring the origin of the suspicious entries](assets/images/validation_table_detail.png)

The second case has more drastic errors. When we enter into the detail for the 2023-03-30 we can see that all entries are duplicated, having two points per time stamp (or almost, with just 1 or 2 seconds of difference). This, combined with the missing data for the 2023-03-31 and the fact we have exactly twice number of records suggest that half of them actually correspond to the next day. Below we see how to edit entries.

But that is not the only problem. Some value cells are also flagged. In this case, the entry has been flagged, most likely, because it is a difference with the previous point too large. What an acceptable difference is defined in the [Variable object](Applications/variable.md). If we scroll further down we can see many other entries having the same problem.

![Exploring more suspicious entries](assets/images/validation_table_suspicious_entries.png)

## What is flagged?

The following list shows the checks that are performed to decide if an entry is suspicious or not:

- The time difference with respect to the previous point is the same (within some tolerance) than the most common time difference for the requested time range.
- The number of entries for the day is correct, i.e. the daily count fraction is 1, based on the same time difference.
- The value is within the minimum and maximum.
- The value does not differ too much with respect to the previous one.

## Manually editing data

Once an entry has been identified as suspicious, there are two things that can be done:

1. Un-check that entry, so that is deactivated and not used in reports. You can deselect full days, not only individual entries.
2. Manually edit the entry

To do this, simply double-click in the cell to edit and change the value to whatever is required. **Be careful when editing dates**, as the format needs to be the right one to be a valid entry.

![Editing an entry](assets/images/validation_edit_entry.png)

## Confirming validation

Once you have deselected the data that is not valid or edited it, then it is ready to be validated. To do this, simply click on the `Validate` button at the bottom-left of the table. You can validate individual days, if you are in the Detailed view, or the whole table.

Data that have been deselected will be validated but set as inactive, meaning that it will not be used for the calculation of the hourly, daily and monthly reports.

Validating the data automatically triggers the report calculation. This calculation might take more or less time depending on the size of the dataset. Once it is concluded, the page refreshes and it should not show any data in the table, as the filters initially selected, which included showing only not-validated data, do not have any match.
