# Installation

There are two basic setups that can be put in place in order to develop and test Paricia locally:

- Virtual environment, used for daily development of the code and the documentation. See section on the [virtual environment setup](#virtual-environment).
- Docker, used to run the tool locally, accessible in the browser as well as to run tests. See section on [docker](#docker-deployment).

## Virtual environment

The normal software development should be done within a virtual environment, where the tools and all the dependencies that Paricia requires are installed. This enables to run the appropriate linters, code formatters, and autocompletion features of the code editor specifically for Paricia. Additionally, it also let you create and develop the documentation.

To setup a virtual environment with all the requirements, navigate to Paricia's root directory in a terminal and run (this should work in all platforms):

```bash
python -m venv .venv
```

This will create an isolated Python environment within a directory called `.venv`. Notice that Paricia requires Python 3.11 or higher to work. Once the environment has been created, you can activate it with:

```ps
.venv\Scripts\activate
```

in Powershell, or

```bash
. .venv/Scripts/activate
```

in Bash. Note the extra `.` and space before `.venv` in this case.

Once in the virtual environment, dependencies for development (linters, formatter, etc.) and documentation, respectively, can be installed with:

```
python -m pip install -r requirements-dev.txt
python -m pip install -r requirements-doc.txt
```

That should be it. The virtual environment should be ready for the development of Paricia and its documentation. Just indicate your code editor which environment you are using in case it does not pick it automatically.

!!! warning "Running Paricia and tests"

    You will not be able to run Paricia itself or the tests from the virtual environment as a TimescaleDB is required for that, which we have not installed. See the [docker deployment](#docker-deployment) section to learn how to do that.

## Docker deployment

Paricia developer's setup requires the use of `docker` to easily manage the different services it is made of, namely the web application itself and the database and make the tool accessible from the web browser. It is also necessary to run the tests.

The steps to setup your system in this case are:

- Install [Docker](https://www.docker.com/)
- In a terminal, run `docker-compose up --build`. This will pull the docker images from the internet, build the local ones and launch the services. Depending on your internet connection, it might take a few minutes to complete.
- After downloading and building the images, Paricia should now be available via a web browser in `http://localhost:8000/`.
- Create **admin** user following the command line instructions described in the [Paricia administrator section](./admin.md#paricia-administrator).

If you want to load initial data (variables, units, stations...):

- In a separate terminal run `docker exec -it <name_of_docker_container> bash` e.g. `docker exec -it paricia-web-1 bash` to start a bash session in the container. You can find the name of the container in the Docker Desktop GUI, or by running `docker ps`.
- Run `python manage.py shell < utilities/load_initial_data.py`.

### Running Paricia after the initial installation

Once the initial setup is done, you can:

- Stop the containers with `docker compose down`
- Re-launch the containers with `docker compose up`. No need to run with the `--build` flag unless some dependency has changed.
- If you want to use the same terminal, you can run the services in detached mode with `docker compose up -d`.

Unless you destroy the docker volume containing the database or manually flush it, the database will persist between subsequent calls to docker compose.

### Building the documentation

The documentation uses [`mkdocs`](https://www.mkdocs.org/). This should have been installed alongside all the other doc-related dependencies if you run `python -m pip install -r requirements-doc.txt`, as described above. There's no need to use `docker` to build the documentation locally.

To test the documentation live and have it rebuilt automatically while you edit the documentation files, run:

```
mkdocs serve -a localhost:8001
```

The reason for explicitly using `localhost:8001` is because port `8000`, the default, will likely be already in use by Paricia web application.

To build the documentation as standalone html files and related resources, run instead:

```
mkdocs build
```

A new directory in the root of the project called `site` would have been created with all the files instead. Open `index.html` in the browser to check this documentation.
