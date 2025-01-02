# Informes

Patricia expone los datos que contiene a través de la página **Informes**.

Esta página contiene un formulario en el lado izquierdo y un gráfico en el derecho, que mostrará los datos seleccionados en el formulario. No se muestran datos en el gráfico al acceder a la página.

![Formulario para completar en la página del informe](../assets/images/reports_form.png)

## Tipos de informes

Hay 5 tipos de informes que se pueden seleccionar:

- Mediciones en bruto: Las mediciones originales, tal como fueron enviadas desde la estación.
- Mediciones validadas: Son las mediciones validadas luego de ser revisadas por un operador, el cual podrá eliminar o cambiar algunas de ellas por resultar incorrectas o sospechosas.
- Horario: Agregación de los datos validados en periodos horarios.
- Diaria: Agregando los datos horarios en periodos diarios.
- Mensual: Agregando los datos diarios en periodos mensuales.

Todos los datos tendrán un informe de mediciones sin procesar, pero los demás estarán disponibles solo si los datos han sido validados.

## Estaciones, variables, y rango de fechas

El usuario solo podrá seleccionar estaciones que pueda ver, lo que significa que los usuarios que **no estén registrados verán solo estaciones que sean públicas**. Los usuarios registrados verán **estaciones públicas e internas**, así como las suyas propias, si las hubiera. Consulte los [Permisos](./permissions.md) para obtener más detalles sobre los permisos de cada usuario.

Después de seleccionar una estación, al usuario se le presentarán las variables disponibles para esa estación, así como el rango de datos.

Una vez que se selecciona la estación, la variable y el rango de fechas elegidos, hay dos opciones: descargar los datos, que descargará el registro como un archivo CSV, o trazar los datos.

## Informe de trama

El gráfico del informe implementa un zoom progresivo, lo que significa que, en general, no mostrará todos los datos dentro del rango (que podrían ser millones de puntos), sino sólo una fracción de ellos, para acelerar la transferencia de datos desde el servidor.

El usuario puede hacer zoom, seleccionar la región de interés y se mostrarán datos más precisos en esa área. Esto puede continuar hasta que los datos mostrados sean el conjunto de datos completo para ese rango. El título del gráfico indica el nivel de agregación, es decir, la diferencia de tiempo promedio entre los puntos de datos que se muestra si no se muestran todos los puntos de datos.

La siguiente figura muestra la temperatura ambiente en un periodo de unas semanas. El título indica un nivel de agregación de alrededor de 23 minutos, lo que significa que los puntos de datos mostrados están separados por 23 minutos en promedio. Tenga en cuenta que **no se realiza ningún procesamiento en los datos** - no hay promedio ni manipulación de otro tipo - simplemente se traza una selección de puntos de datos existentes en todo el rango. En otras palabras, si la separación de datos original fue de 5 minutos, entonces un nivel de agregación de 23 minutos significa que solo se traza 1 punto entre 4 o 5.

![Gráfico con agregación de datos de 23,6 minutos](../assets/images/high_aggregation.png)

En el siguiente gráfico, hemos ampliado un poco y ahora la separación media es de 15 min.

![Gráfico con agregación de datos de 15 minutos](../assets/images/some_aggregation.png)

En el gráfico final, el zoom es lo suficientemente alto como para que no sea necesaria ninguna agregación.

![Gráfico sin agregación de datos](../assets/images/no_aggregation.png)

En todos los casos, para volver al rango completo, utilice las herramientas en la esquina superior derecha del gráfico o haga doble clic en él.

## Picos faltantes

El enfoque elegido para seleccionar los datos a trazar (sólo omitiendo puntos) es extremadamente rápido ya que no se requiere procesamiento de datos, pero tiene algunos inconvenientes. En particular, como la visualización de los datos omite algunos puntos, cuantos más puntos, mayor será el nivel de agregación, es posible que se pierdan algunas características de los datos.

Por ejemplo, si ampliamos la primera parte de la serie, podemos ver algunos puntos de datos (muy probablemente incorrectos) que disparan hasta 50. Estos no eran visibles en la vista general.

![Trazar con picos cuando hay suficiente zoom](../assets/images/spikes.png)
