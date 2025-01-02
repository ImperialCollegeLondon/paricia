# Validación

La validación es el proceso mediante el cual un operador revisa los datos ingeridos por la base de datos y los descarta, modifica o acepta y, por lo tanto, se utiliza para crear informes.

## Seleccionando los datos a validar

El proceso comienza seleccionando los datos a validar en la página de validación. **Solo los usuarios registrados con permisos de cambio para una estación en particular pueden validar los datos de esa estación**. Una vez seleccionada la estación, se muestran las variables disponibles para esa estación, así como otros filtros basados en sus valores, rango de fechas o estado. De forma predeterminada, todos los datos no validados para la variable y estación seleccionadas se muestran una vez que se hace clic en el botón "Enviar".

![Selección de los datos a validar](../assets/images/validation_selector.png)

!!! consejo "Minimizar el intervalo de fechas"

Si bien la base de datos puede manejar consultas de millones de entradas a la vez, dichos datos deberán manipularse, analizarse previamente en busca de valores sospechosos y luego enviarse desde el servidor al navegador e incluirse en la tabla y el gráfico debajo. Por lo tanto, es importante que los usuarios elijan sólo el rango de fechas que les interesa explorar para minimizar los tiempos de carga y hacer que todo el proceso sea más fluido.

## El informe diario

Después de enviar la solicitud de datos, se muestra una tabla con un informe diario, así como un gráfico debajo. Ambos son útiles para identificar entradas sospechosas en los datos que deben corregirse o descartarse manualmente.

Por ejemplo, la siguiente imagen muestra que hay un problema el primer día, 2023-03-14, resaltando en rojo la celda problemática. En particular, muestra que, según la diferencia horaria esperada entre puntos de datos (tomada como la moda de la diferencia horaria para todos los datos en el rango), solo se espera el 80% de los datos para este día. Además, ese día hay 2 entradas sospechosas.

![Informe diario que muestra algunas entradas sospechosas](../assets/images/validation_table.png)

Si nos desplazamos hacia abajo en la tabla, podemos ver que hay más problemas con estos datos. El último día sólo tiene el 21% de los datos esperados, dos entradas sospechosas y un problema con el campo `valor`. El penúltimo es aún peor, con el doble de entradas de las que debería y más de 303 de ellas sospechosas. El gráfico siguiente también apunta a un problema potencial: una brecha en la serie de datos.

![Informe diario con más entradas sospechosas y la trama](../assets/images/validation_table_other_errors.png)

## El detalle del día

Para saber exactamente de qué se tratan las entradas sospechosas, podemos seleccionar el día concreto en el selector de fechas de la esquina inferior derecha. Las entradas del día seleccionado se mostrarán en otra pestaña dentro de la misma tabla.

Podemos encontrar las entradas sospechosas, 2 en el primer caso, desplazándonos por la tabla en busca de celdas marcadas. Podemos ver que dos entradas están marcadas juntas, en la columna de tiempo. Esto indica un problema con el momento de estas entradas. Se puede observar que el problema es que la periodicidad no es la correcta, con una separación de 2 y 3 minutos respecto al punto anterior, mientras que esa separación debería ser de 5 min según los metadatos de la estación. Lo más probable es que el punto de la línea 95 no esté allí.

![Explorando el origen de las entradas sospechosas](../assets/images/validation_table_detail.png)

El segundo caso tiene errores más drásticos. Cuando entramos en el detalle del 30-03-2023 podemos ver que todas las entradas están duplicadas, teniendo dos puntos por marca de tiempo (o casi, con apenas 1 o 2 segundos de diferencia). Esto, combinado con los datos faltantes para el 31-03-2023 y el hecho de que tenemos exactamente el doble de registros, sugiere que la mitad de ellos en realidad corresponden al día siguiente. A continuación vemos cómo editar las entradas.

Pero ese no es el único problema. Algunas celdas de valores también están marcadas. En este caso, la entrada ha sido marcada, muy probablemente, porque hay una diferencia demasiado grande con el punto anterior. La diferencia aceptable se define en [Objeto variable] (Aplicaciones/variable.md). Si nos desplazamos hacia abajo podremos ver muchas otras entradas que tienen el mismo problema.

![Explorando más entradas sospechosas](../assets/images/validation_table_suspicious_entries.png)

## ¿Qué está marcado?

La siguiente lista muestra las comprobaciones que se realizan para decidir si una entrada es sospechosa o no:

- La diferencia horaria respecto al punto anterior es igual (dentro de una cierta tolerancia) que la diferencia horaria más habitual para el rango horario solicitado.
- El número de entradas del día es correcto, es decir, la fracción de recuento diario es 1, basándose en la misma diferencia horaria.
- El valor está dentro del mínimo y máximo.
- El valor no difiere demasiado respecto al anterior.

## Editar datos manualmente

Una vez que una entrada ha sido identificada como sospechosa, se pueden hacer dos cosas:

1. Desmarca esa entrada, para que quede desactivada y no utilizada en los informes. Puedes deseleccionar días completos, no solo entradas individuales.
2. Edite manualmente la entrada

Para hacer esto, simplemente haga doble clic en la celda para editar y cambiar el valor al que sea necesario. **Tenga cuidado al editar fechas**, ya que el formato debe ser el correcto para que sea una entrada válida.

![Editando una entrada](../assets/images/validation_edit_entry.png)

## Confirmando validación

Una vez que hayas deseleccionado los datos que no son válidos o los hayas editado, entonces estará listo para ser validado. Para hacer esto, simplemente haga clic en el botón "Validar" en la parte inferior izquierda de la tabla. Puedes validar días individuales, si estás en la vista Detallada, o toda la tabla.

Los datos que hayan sido deseleccionados serán validados pero fijados como inactivos, es decir, no serán utilizados para el cálculo de los informes horarios, diarios y mensuales.

La validación de los datos activa automáticamente el cálculo del informe. Este cálculo puede llevar más o menos tiempo según el tamaño del conjunto de datos. Una vez concluido, la página se actualiza y no debería mostrar ningún dato en la tabla, ya que los filtros seleccionados inicialmente, que incluían mostrar solo datos no validados, no tienen ninguna coincidencia.
