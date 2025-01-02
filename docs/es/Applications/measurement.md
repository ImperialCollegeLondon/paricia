# Medición

## Introducción

Todos los datos que se introducen o procesan en Paricia toman la forma de objetos de `Medición` o `Informe`. A diferencia de otros elementos de Paricia, **estos no están pensados ​​para crearse manualmente a través de las páginas de administración**, sino en segundo plano al importar o validar datos.

!!! advertencia "No edite las mediciones en la página de administración"

**Se desaconseja editar mediciones directamente en las páginas de administración**, ya que puede generar inconsistencias entre los datos sin procesar, validados e informados. En su lugar, utilice las herramientas de validación. Consulte [la sección de validación](../validation.md)

En ambos casos, representan un único punto de datos en una serie temporal, correspondiente a una `Variable` específica en una `Estación` específica. Solo los datos correspondientes a estaciones **públicas** estarán disponibles para su verificación en el caso de usuarios anónimos, mientras que los usuarios registrados también podrán verificar los datos de estaciones **internas**.

En el caso de `Reports`, el punto de datos es una magnitud posprocesada promediada (o acumulada) en períodos de tiempo horarios, diarios y mensuales. Solo se utilizan los datos que han sido validados al calcular los informes. Los datos de `Report` son los que se utilizan en la vista de informe para generar gráficos y se pueden descargar. Por lo general, es lo que a la mayoría de las personas les interesará verificar.

`Measurement` representa un punto de datos de entrada cargado desde un archivo, con todas sus propiedades y metadatos. La mayoría de sus propiedades se pueden editar durante el proceso de validación, pero los datos originales en bruto siempre se conservan y se pueden recuperar cuando/si es necesario.

Ambos objetos de tipo derivan de una clase abstracta `MeasurementBase` que contiene los elementos comunes, que a su vez deriva de `TimescaleModel`. Esta clase principal superior es la que permite toda la gestión eficiente de series temporales de los datos en Paricia.

![Diagrama UML de los modelos de la aplicación Measurement.](../images/measurement.png)

## Componentes

::: measurement.models.MeasurementBase
    options:
      heading_level: 3
      show_bases: True
      members: None
      show_root_full_path: False

::: measurement.models.Measurement
    options:
      heading_level: 3
      show_bases: False
      members: None
      show_root_full_path: False

::: measurement.models.Report
    options:
      heading_level: 3
      show_bases: False
      members: None
      show_root_full_path: False
