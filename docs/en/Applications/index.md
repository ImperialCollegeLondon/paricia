# Paricia applications

All functionality in Parcia is contained in several Django applications, each of them, in turn, including one or more database models that define that functionality.

- [**Formatting**](formatting.md): Definitions of the different file formats that can be imported, including specifics around delimiters, headers etc.
- [**Variable:**](variable.md) Information about measured variables including units, max/min allowed values etc.
- [**Sensor:**](sensor.md) Information on physical sensors including brand and type.
- [**Station:**](station.md) Everything to do with physical stations including their location, region, ecosystem etc.
- [**Importing:**](importing.md) Entries are created in this app when datasets are imported, storing information on the the raw data file itself, the user, time of import etc.
- [**Measurement:**](measurement.md) The actual time-series data is stored here when raw data files are imported.

The objects for all of these apps, except for **Measurements**, can be managed by registered users via the corresponding forms in the front end, and for superusers also via the Admin pages.

## Other utilities

In addition to the applications containing the actual functionality, the project file structure has other directories that are of interest only for developers.

- The top-level directory contains various config files and directories for git, github, docker and pip.
- Each django app is in a subdirectory and `djangomain` contains the main django settings, views and urls.
- The **Management** app contains the custom user model, base permission classes and base views, used by all other apps to save boilerplate code.
- The `static` directory contains the static files for the project.
- The `templates` directory contains the templates for the project, used to render the different views in the browser.
- The `utilities` directory contains helper functions for the project.
- The `tests` directory contains all unit tests for the project.
