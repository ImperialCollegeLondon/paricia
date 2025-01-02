# Seguro de calidad

## Pruebas

Las pruebas se ejecutan con `python enable.py test` desde el interior del contenedor acoplable (consulte las [instrucciones de instalación](./installation.md) para ver cómo hacerlo).

Para que eso funcione, es necesario instalar dependencias relacionadas con el desarrollo. Ya deberían estarlo, pero si no es así, entra en el contenedor y ejecuta:

```bash
python -m pip install -r requirements-dev.txt
```

Las pruebas se crean utilizando el marco "unittest". Lea la [documentación de Pruebas en Django](https://docs.djangoproject.com/en/5.1/topics/testing/) sobre cómo escribir pruebas para una aplicación Django.

### Ejecutar pruebas seleccionadas

El comando anterior ejecutará todas las pruebas disponibles. Sin embargo, a menudo (especialmente durante la depuración) querrás ejecutar sólo pruebas específicas. Para hacerlo, escriba las pruebas o grupo o pruebas que desea ejecutar usando la notación de puntos para indicar la ruta a la prueba:

- Ejecutar una prueba específica, por ejemplo. `test_launch_reports_calculation`
```bash
python manage.py test tests.measurement.test_reporting.TestReporting.test_launch_reports_calculation
```
- Ejecutar todas las pruebas dentro de una clase de prueba, por ejemplo. `TestReporting`
```bash
python manage.py test tests.measurement.test_reporting.TestReporting
```
- Ejecutar todas las pruebas dentro de un directorio, por ejemplo. `measurement`, dentro del directorio `test`
```bash
python manage.py test tests.measurement
```

## Integración continua

### Ganchos de confirmación previa

Los enlaces de confirmación previa están configurados para ejecutar comprobaciones de calidad del código (`ruff` y `mypy`) antes de la confirmación. Para ejecutarlos localmente, necesitará "pip install pre-commit" y luego "pre-commit install". Ahora, las herramientas de control de calidad se ejecutarán automáticamente con cada confirmación.

### Flujos de trabajo de GitHub

Los flujos de trabajo de Github están configurados para ejecutar lo siguiente automáticamente:

- Con cada envío a una sucursal con una solicitud de extracción abierta:
- Ejecute la confirmación previa en todos los archivos (como ejecutar localmente `pre-commit run --all-files`). Esto se hace en un servicio externo, [precommit.ci](https://pre-commit.ci/)
- Ejecute el conjunto de pruebas completo.
- Consultar enlaces en la documentación.
- Construir la documentación (no implementarla)
- Cuando se crea una nueva versión en GitHub:
- Todo lo anterior, y en caso de tener éxito,
- La nueva versión de la documentación está publicada en [GitHub Pages](https://imperialcollegelondon.github.io/paricia/)
- Se crea una imagen acoplable para Paricia y se publica en el [Registro de contenedores de GitHub] (https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)

Si alguna implementación de Paricia está buscando nuevas versiones en el registro, la nueva versión podría desencadenar una actualización automática de dicha implementación.

Además, el repositorio de Paricia está configurado para recibir actualizaciones automáticas de paquetes y dependencias a través de bots `dependabot` y `pre-commit`. Periódicamente, abrirán solicitudes de extracción con las versiones actualizadas y, si las comprobaciones anteriores tienen éxito, se fusionarán automáticamente. Si bien a veces es necesaria la intervención manual si las versiones actualizadas no funcionan, este proceso ayuda a mantener Paricia actualizada y simplifica el trabajo de los mantenedores.
