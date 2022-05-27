# Paricia

Hydroclimatic data management system.

This README is a work in progress.

## Getting started

If installing this system from scratch:

- Run `docker-compose up --build` (requires [Docker](https://www.docker.com/) to be running)
- In a separate terminal run `docker exec -it <name_of_docker_container> bash` e.g. `docker exec -it paricia_web_1 bash` to start a bash session in the container. You can find the name of the container in the Docker Desktop GUI, or by running `docker container ls`. 
- Run `python manage.py makemigrations` to create initial migrations for each app.
- Run `python manage.py migrate` to execute the migrations.
- If you want to load initial data (variables, units, stations...) run `python manage.py shell < scripts/load_initial_data.py`
