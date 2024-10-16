# Paricia applications

All functionality in Parcia is contained in several Django applications, each of them, in turn, including one or more database models that define that functionality.

These pages describe in more detail all these models, what they are for and how they relate to each other. **All registered users can create new models for these applications via the Admin pages**.

- [**Formatting**](formatting.md): Definitions of the different file formats that can be imported, including specifics around delimiters, headers etc.
- [**Variable:**](variable.md) Information about measured variables including units, max/min allowed values etc.
- [**Sensor:**](sensor.md) Information on physical sensors including brand and type.
- [**Station:**](station.md) Everything to do with physical stations including their location, region, ecosystem etc.
- [**Importing:**](importing.md) Entries are created in this app when datasets are imported, storing information on the the raw data file itself, the user, time of import etc.
- [**Measurement:**](measurement.md) The actual time-series data is stored here when raw data files are imported.
