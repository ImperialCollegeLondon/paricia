# Original iMHEA interface

## Instructions

- `docker-compose up --build` to start the containers
- `docker exec -it paricia_web_1 bash` to start a session in the web container (replace `paricia_web_1` with the name of the container, it may be different)
- `python manage.py createsuperuser` to create a superuser
- `python manage.py makemigrations` and `python manage.py migrate` to make migrations and apply them
- Open the server at `localhost:8000/` in the browser and login in the top right
- If you want to load initial data (variables, units, stations...) go to Mantenimiento -> Carga inicial (Maintenance -> Initial Upload) and click on each radio button _starting with the first (Variable:Unidades) and going down one by one_ clicking "Cargar seleccionado" each time
- You should then be able to browse e.g. Estacion -> Estacion to see a list of stations.

Note - data upload won't work in this branch, but would be achieved by coming to Importacion de dataos -> importar Archivo.
