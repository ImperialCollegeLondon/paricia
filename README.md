✨ ➡️ [**LINK TO DEVELOPMENT PROJECT BOARD**](https://github.com/ImperialCollegeLondon/paricia/projects/1) ⬅️ ✨

# Paricia

Hydroclimatic data management system.

This README is a work in progress.

## Getting started

If installing this system from scratch:

- Run `docker-compose up --build` (requires [Docker](https://www.docker.com/) to be running)
- If you want to load initial data (variables, units, stations...):
  - In a separate terminal run `docker exec -it <name_of_docker_container> bash` e.g. `docker exec -it paricia_web_1 bash` to start a bash session in the container. You can find the name of the container in the Docker Desktop GUI, or by running `docker container ls`.
  - Run `python manage.py shell < utilities/load_initial_data.py`.

## User roles and permissions

When the project is initialised, data migrations automatically create several groups
for users with different permissions:

- User manager: Able to add, change, delete, view users.
- Maintainer: Able to add, change, delete, view data in the database, but not users.
- Contributor: Able to Add new measurement data to the database by uploading data files.
- Read only: Given view permission for all data but not users.

Django superusers can be created in the usual way and have all permissions.
The groups listed above are _not_ mutually exclusive. i.e. most users who are in the
**Contributors** group would also be in the **Read only** group so they are able to view
the data they add.
