✨ ➡️ [**LINK TO DEVELOPMENT PROJECT BOARD**](https://github.com/ImperialCollegeLondon/paricia/projects/1) ⬅️ ✨

# Paricia

Hydroclimatic data management system.

This README is a work in progress.

## Getting started

If installing this system from scratch:

- Run `docker-compose up --build` (requires [Docker](https://www.docker.com/) to be running)
- If you want to load initial data (variables, units, stations...):
  - In a separate terminal run `docker exec -it <name_of_docker_container> bash` e.g. `docker exec -it paricia-web-1 bash` to start a bash session in the container. You can find the name of the container in the Docker Desktop GUI, or by running `docker container ls`.
  - Run `python manage.py shell < utilities/load_initial_data.py`.
  - Create **admin** user running `python manage.py createsuperuser`.

## Database Schema

### The database is split into several applications

- **Station:** Everything to do with physical stations including their location, region, ecosystem etc.
- **Sensor:** Information on physical sensors including brand and type.
- **Variable:** Information about measured variables including units, max/min allowed values etc.
- **Importing:** Entries are created in this app when datasets are imported, storing information on the the raw data file itself, the user, time of import etc.
- **Formatting:** Definitions of the different file formats that can be imported, including specifics around delimiters, headers etc.
- **Measurement:** The actual time-series data is stored here when raw data files are imported. A separate model (table) exists for each variable type.
- **Management:** User management.

The first four models are shown below (formatting, measurement and management are ommitted to keep the diagram simple).

![Flowchart showing the database schema](static/images/database_viz.png)

To regenerate the image above:

- Install graphviz and pygraphviz. Simplest is often `conda install pygraphviz` to get the necessary C extensions at the same time.
- `python manage.py graph_models importing station sensor variable -R -g -o viz.pdf`. Replace the positional arguments for the apps to be included.

### Non-obvious links and associations

- A `DataImportTemp` object is created when a data file is initially uploaded and functions are run to check its validity and the time range, variable type and station involved, and therefore whether any data would be overwritten. A `DataImportFull` object is created to confirm the import, creating entries in the Measurement app. Each `DataImportFull` is related to one `DataImportTemp` object.
- Each `Sensor` is linked to a `Station` and the `Variable` it measures via the `SensorInstallation` object.

## User roles and permissions

When the project is initialised, data migrations automatically create several groups
for users with different permissions:

- **User manager:** Able to add, change, delete, view users.
- **Maintainer:** Able to add, change, delete, view data in the database, but not users.
- **Contributor:** Able to Add new measurement data to the database by uploading data files.
- **Read only:** Given view permission for all data but not users.

Django superusers can be created in the usual way and have all permissions.
The groups listed above are _not_ mutually exclusive. i.e. most users who are in the
**Contributors** group would also be in the **Read only** group so they are able to view
the data they add.

## Project structure

- The top-level directory contains various config files and directories for git, github, docker and pip.
- Each django app is in a subdirectory and `djangomain` contains the main django settings, views and urls.
- The `static` directory contains the static files for the project.
- The `templates` directory contains the templates for the project.
- The `utilities` directory contains helper functions for the project.
- The `tests` directory contains all unit tests for the project.

### Unused code

This project is based on a previous codebase that includes many more features in many more apps.
It is hoped that over time these features will be refactored and included again in the system.
Rather than removing the associated code, it has been moved to `unused_apps`.
Similarly, there are `templates/unused_templates` and `utilities/unused_scripts`.

## Development

Paricia is developed at [Imperial College London](https://www.imperial.ac.uk/) by the Research Software Engineering team within the Research Computing Group.
The project is coordinated by [Prof. Wouter Buytaert](https://www.imperial.ac.uk/people/w.buytaert).

The code was originally based on the iMHEA platform - Plataforma para la **I**niciativa Regional de **M**onitoreo **H**idrológico de **E**cosistemas **A**ndinos. We are grateful to the following instututions for the development of iMHEA and for sharing their code to use as a starting point for Paricia:

- Fondo para la Proteccion del Agua (FONAG), Ecuador.
- Empresa Pública Metropolitana de Agua Potable Y Saneamiento de Quito (EPMAPS)m Ecuador.

### Tests

The tests are run with `python manage.py test` from inside the docker container.

### Continuous integration

Pre-commit hooks are set up to run code quality checks (isort and black) before committing. To run these locally, you will need to `pip install pre-commit` then `pre-commit install`.
Github workflows are set up to run the pre-commit actions and the tests automatically on every push action.
Run before commit: `pre-commit run --all-files`