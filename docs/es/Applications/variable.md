# Variable

## Introducción

La aplicación Variable se ocupa de las variables que pueden ser ingeridas por Paricia, desde qué son y qué unidades utilizan hasta recursos para ayudar en el proceso de validación. Especialmente importantes en este proceso de validación serán:

- los valores máximos y mínimos que la variable puede tomar de forma realista (estos son campos obligatorios)
- la variabilidad máxima entre puntos de datos consecutivos
- la diferencia estadística máxima respecto de la serie permitida para un punto de datos antes de que se considere un outlier
- la fracción de valores faltantes que se permiten al calcular informes

![Diagrama UML de los modelos de la aplicación Variable.](../images/variable.png)

## Componentes

::: variable.models.Unit
    options:
      heading_level: 3
      show_bases: False
      members: None
      show_root_full_path: False

::: variable.models.Variable
    options:
      heading_level: 3
      show_bases: False
      members: None
      show_root_full_path: False

::: variable.models.SensorInstallation
    options:
      heading_level: 3
      show_bases: False
      members: None
      show_root_full_path: False
