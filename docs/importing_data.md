# Importing Data

## Submit the data import

Data import is done via Paricia Admin. Just click in `Add` or in `Add Data Import` in the corresponding screen, and a new form will open for you to complete:

![Form to import new data](images/importing_add_data.png)

The form contains several fields to be filled by the users and a few others that will be populated automatically when the data to import is completed.

The Station, Format and Data File are, obviously, critical and the import will likely fail if the wrong combination is chosen - eg. if the wrong format is chosen or the data file contains variables that the Station is not supposed to have.

For the Station, the user will only be able to choose those for which they have `change` permission. For the Format, the will be able to choose their own formats and those labelled as `public`.

Once the form is complete, click `Save` at the bottom of the page and the import process will start.

## Process the data

The data is ingested asyncronously, so the user can keep using Paricia. The status of the data import object indicate how the process is going:

- **Not Queued**: The data ingestion has not started, yet.

![Data ingestion not queued](images/importing_not_queued.png)

- **Queued**: The data ingestion has started. Data file has been opened and is being processed.

![Data ingestion queued](images/importing_queued.png)

- **Completed**: The data ingestion has completed successfully. Information on the start and end dates of the data, as well as the number of records, will appear updated

![Data ingestion completed](images/importing_completed.png)

- **Failed**: The data ingestion failed. Information on what went wrong should appear in the log box at the bottom of the data import detail. Try to fix the issues, based on the feedback provided, check the box `Reprocess Data`, and save the form again to trigger another data ingestion process.

![Data ingestion failed](images/importing_failed.png)

Once the data has been ingested successfully, it will be available to validate in the [Validation screen](validation.md) and in the Report screen, if the Station it belongs to is labelled as public or internal.
