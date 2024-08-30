# WIP: Database and code structure

## The database is split into several applications

- **Station:** Everything to do with physical stations including their location, region, ecosystem etc.
- **Sensor:** Information on physical sensors including brand and type.
- **Variable:** Information about measured variables including units, max/min allowed values etc.
- **Importing:** Entries are created in this app when datasets are imported, storing information on the the raw data file itself, the user, time of import etc.
- **Formatting:** Definitions of the different file formats that can be imported, including specifics around delimiters, headers etc.
- **Measurement:** The actual time-series data is stored here when raw data files are imported. A separate model (table) exists for each variable type.
- **Management:** User management.

## Non-obvious links and associations

- A `DataImportTemp` object is created when a data file is initially uploaded and functions are run to check its validity and the time range, variable type and station involved, and therefore whether any data would be overwritten. A `DataImportFull` object is created to confirm the import, creating entries in the Measurement app. Each `DataImportFull` is related to one `DataImportTemp` object.
- Each `Sensor` is linked to a `Station` and the `Variable` it measures via the `SensorInstallation` object.

## Project structure

- The top-level directory contains various config files and directories for git, github, docker and pip.
- Each django app is in a subdirectory and `djangomain` contains the main django settings, views and urls.
- The `static` directory contains the static files for the project.
- The `templates` directory contains the templates for the project.
- The `utilities` directory contains helper functions for the project.
- The `tests` directory contains all unit tests for the project.
