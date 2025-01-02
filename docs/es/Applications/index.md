# Aplicaciones de Paricia

Toda la funcionalidad de Parcia está contenida en varias aplicaciones de Django, cada una de ellas, a su vez, incluye uno o más modelos de base de datos que definen esa funcionalidad.

- [**Formatting**](formatting.md): definiciones de los diferentes formatos de archivo que se pueden importar, incluyendo detalles sobre delimitadores, encabezados, etc.
- [**Variable:**](variable.md) Información sobre las variables medidas, incluyendo unidades, valores máximos/mínimos permitidos, etc.
- [**Sensor:**](sensor.md) Información sobre sensores físicos, incluyendo marca y tipo.
- [**Station:**](station.md) Todo lo relacionado con las estaciones físicas, incluida su ubicación, región, ecosistema, etc.
- [**Importing:**](importing.md) Las entradas se crean en esta aplicación cuando se importan conjuntos de datos, almacenando información sobre el archivo de datos sin procesar, el usuario, el momento de la importación, etc.
- [**Measurement:**](measurement.md) Los datos de series temporales reales se almacenan aquí cuando se importan archivos de datos sin procesar.

Los objetos de todas estas aplicaciones, excepto **Measurements**, pueden ser administrados por usuarios registrados a través de los formularios correspondientes en el front-end, y para superusuarios también a través de las páginas de administración.

## Otras utilidades

Además de las aplicaciones que contienen la funcionalidad real, la estructura de archivos del proyecto tiene otros directorios que son de interés solo para los desarrolladores.

- El directorio de nivel superior contiene varios archivos de configuración y directorios para git, github, docker y pip.
- Cada aplicación de Django se encuentra en un subdirectorio y `djangomain` contiene las configuraciones, vistas y URL principales de Django.
- La aplicación **Management** contiene el modelo de usuario personalizado, las clases de permisos base y las vistas base, que utilizan todas las demás aplicaciones para guardar el código repetitivo.
- El directorio `static` contiene los archivos estáticos del proyecto.
- El directorio `templates` contiene las plantillas del proyecto, que se utilizan para representar las diferentes vistas en el navegador.
- El directorio `utilities` contiene funciones auxiliares para el proyecto.
- El directorio `tests` contiene todas las pruebas unitarias del proyecto.`az