# Instalación

Hay dos configuraciones básicas que se pueden implementar para desarrollar y probar Paricia localmente:

- Entorno virtual, utilizado para el desarrollo diario del código y la documentación. Consulte la sección sobre [configuración del entorno virtual](#entorno-virtual).
- Docker, utilizado para ejecutar la herramienta localmente, accesible en el navegador así como para ejecutar pruebas. Consulte la sección sobre [docker](#docker-deployment).

## Entorno virtual

El desarrollo normal de software debe realizarse dentro de un entorno virtual, donde se instalan las herramientas y todas las dependencias que requiere Paricia. Esto permite ejecutar los linters, formateadores de código y funciones de autocompletado apropiados del editor de código específicamente para Paricia. Además, también le permite crear y desarrollar la documentación.

Para configurar un entorno virtual con todos los requisitos, navegue hasta el directorio raíz de Paricia en una terminal y ejecute (esto debería funcionar en todas las plataformas):

```bash
python -m venv .venv
```

Esto creará un entorno Python aislado dentro de un directorio llamado `.venv`. Tenga en cuenta que Paricia requiere Python 3.11 o superior para funcionar. Una vez creado el entorno, podrás activarlo con:

```ps
.venv\Scripts\activate
```

en Powershell, o

```bash
source .venv/bin/activate
```

en Bash/Zsh.

Una vez en el entorno virtual se pueden instalar dependencias para desarrollo (linters, formateador, etc.) y documentación, respectivamente, con:

```
python -m pip install -r requirements-dev.txt
python -m pip install -r requirements-doc.txt
```

Entonces, la propia paricia se puede instalar con:

```
python -m pip install -e .
```

Eso debería ser todo. El entorno virtual deberá estar preparado para el desarrollo de Paricia y su documentación. Simplemente indique a su editor de código qué entorno está utilizando en caso de que no lo seleccione automáticamente.

!!! Advertencia "Ejecutando Paricia y pruebas"

No podrá ejecutar Paricia ni las pruebas desde el entorno virtual porque esto requiere TimescaleDB, que no está instalado como parte del entorno virtual. Consulte la sección [implementación de Docker](#docker-deployment) para aprender cómo hacerlo.

## Implementación de Docker

La configuración del desarrollador de Paricia requiere el uso de "docker" para administrar fácilmente los diferentes servicios que lo componen, es decir, la aplicación web en sí y la base de datos, y hacer que la herramienta sea accesible desde el navegador web. También es necesario realizar las pruebas.

Los pasos para configurar su sistema en este caso son:

- Instalar [Docker] (https://www.docker.com/)
- En una terminal, ejecute `docker-compose up --build`. Esto extraerá las imágenes de la ventana acoplable de Internet, creará las locales e iniciará los servicios. Dependiendo de su conexión a Internet, es posible que tarde unos minutos en completarse.
- Después de descargar y crear las imágenes, Paricia ahora debería estar disponible a través de un navegador web en `http://localhost:8000/`.
- Cree un usuario **admin** siguiendo las instrucciones de la línea de comando descritas en la [sección Administrador de Paricia](./admin.md#paricia-administrator).

Si quieres cargar datos iniciales (variables, unidades, estaciones...):

- En una terminal separada, ejecute `docker exec -it <name_of_docker_container> bash`, p. `docker exec -it paricia-web-1 bash` para iniciar una sesión bash en el contenedor. Puede encontrar el nombre del contenedor en la GUI de Docker Desktop o ejecutando `docker ps`.
- Ejecute `python enable.py shell <utilidades/load_initial_data.py`.

### Ejecutando Paricia después de la instalación inicial

Una vez realizada la configuración inicial, puede:

- Detener los contenedores con `docker compose down`
- Reiniciar los contenedores con `docker compose up`. No es necesario ejecutar con el indicador `--build` a menos que alguna dependencia haya cambiado.
- Si desea utilizar el mismo terminal, puede ejecutar los servicios en modo independiente con `docker compose up -d`.

A menos que destruya el volumen de Docker que contiene la base de datos o lo vacíe manualmente, la base de datos persistirá entre llamadas posteriores a Docker Compose.

### Construyendo la documentación

La documentación utiliza [`mkdocs`](https://www.mkdocs.org/). Esto debería haberse instalado junto con todas las demás dependencias relacionadas con documentos si ejecuta `python -m pip install -r requisitos-doc.txt`, como se describe anteriormente. No es necesario utilizar `docker` para crear la documentación localmente.

Debido a la naturaleza multilingüe de la documentación, la forma normal de servir la documentación (a través de los comandos 'mkdocs build' y 'mkdocs serve') no funcionará aquí. En su lugar, debe utilizar los siguientes comandos para crear la documentación:

```
mkdocs build -f config/en/mkdocs.yml
mkdocs build -f config/es/mkdocs.yml
```

La documentación ahora está disponible en la carpeta sites/. Desde allí, puede servirla con el servidor http de Python:

```
cd sites/
python3 -m http.server 8001
```

Ahora se puede acceder al sitio de documentación a través de un navegador web en http://localhost:8001

La razón para usar explícitamente `localhost:8001` es porque el puerto `8000`, el predeterminado, probablemente ya esté en uso por la aplicación web Paricia.