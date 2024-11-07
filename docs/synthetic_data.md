# Synthetic data

Synthetic data can be added to the database for benchmarking purposes using one of the scenarios in `utilities/benchmarking` or creating one of your own. To do so:

- Populate the database with some initial data for the `Station`, `Variable` and all the required models (see the *Getting Started* section).
- Install the development dependencies (read the *Tests* section)
- Run your desired synthetic data scenario.

If you run one of the built in ones, you should see a progressbar for the process and, if you log in into the Django Admin of Paricia (`http://localhost:8000/admin`), then you will see the records for the `Measurements` model increasing.
