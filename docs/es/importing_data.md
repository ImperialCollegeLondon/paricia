# Importación de datos

La razón de ser de Paricia es almacenar y facilitar el acceso a los datos hidrológicos. Por lo tanto, uno de sus componentes principales, que depende de todo lo demás, es el proceso de ingesta de datos.

## Enviar la importación de datos

La importación de datos se realiza a través de la lista de importación de Paricia, haciendo clic en el botón `Nuevo` en la parte superior de la página.

![Lista de importación de datos](../assets/images/import_list.png)

Se abrirá un formulario en una nueva página, que contiene varios campos para que los usuarios completen.

![Formulario para importar nuevos datos](../assets/images/importing_add_data.png)

### Formato

El **Formato** es la opción más importante a elegir. Si el formato no es correcto, el proceso de importación fallará, con suerte con un mensaje de error significativo que indique qué salió mal. Si no está seguro sobre qué formato elegir, puede explorar las opciones disponibles en el menú `Formato -> Formato` y abrir los formatos sobre los que desea obtener más información.

**Dentro de la página de formato específico**, entre los diferentes ajustes como las columnas de fecha y hora, separador, etc. encontrará las **Clasificaciones**, es decir, la lista de variables y las columnas desde las que se importarán si se utiliza ese formato. **Los índices de las columnas comienzan en 0**, por lo que una variable importada de la columna número 2, por ejemplo, se importará desde la 3.ª columna del archivo. Asegúrese de que esta lista de clasificaciones coincida con la información que desea importar desde el archivo de datos.

La siguiente figura muestra las clasificaciones disponibles para un formato en particular:

![Lista de clasificaciones de variables en columnas](../assets/images/classifications.png)

Al hacer clic en el `id` de cada clasificación, se mostrará más información sobre esa clasificación en particular. Tenga en cuenta que es posible que no tenga permiso para ver los detalles de esa clasificación.

### Estación

Para la Estación, el usuario solo podrá elegir aquellas para las que tenga permiso `cambiar`. Para el Formato, podrá elegir sus propios formatos y aquellos etiquetados como `públicos`.

La estación debe estar completa, es decir, debe tener todos los campos obligatorios llenos, algo que podría no ser el caso si la estación fue importada a Paricia. Un campo que suele faltar es el `timezone`, si ese fuera el caso, se le notificará al intentar guardar la importación de datos. Para solucionarlo, simplemente vaya a la página de la estación - `Station -> Station` en el menú superior - y actualice los campos que faltan.

## Procesar los datos

Una vez que el formulario esté completo, haga clic en `Save` en la parte superior de la página y comenzará el proceso de importación. Los datos se ingieren de forma asincrónica, por lo que el usuario puede seguir utilizando Paricia. El estado del objeto de importación de datos indica cómo va el proceso:

- **Not Queued**: La ingesta de datos aún no ha comenzado.

![Ingestión de datos no en cola](../assets/images/importing_not_queued.png)

- **Queued**: La ingesta de datos ha comenzado. El archivo de datos se ha abierto y se está procesando.

![Ingestión de datos en cola](../assets/images/importing_queued.png)

- **Completado**: la ingesta de datos se ha completado correctamente. La información sobre las fechas de inicio y finalización de los datos **en la zona horaria local del usuario**, así como la cantidad de registros, aparecerán actualizadas

![Ingestión de datos completada](../assets/images/importing_completed.png)

- **Error**: la ingesta de datos falló. La información sobre lo que salió mal debería aparecer en el cuadro de registro en la parte inferior del detalle de la importación de datos. Intente solucionar los problemas, según los comentarios proporcionados, marque la casilla "Reprocesar datos" y guarde el formulario nuevamente para activar otro proceso de ingesta de datos.

![Error en la ingesta de datos](../assets/images/importing_failed.png)

Una vez que los datos se hayan ingerido correctamente, estarán disponibles para su validación en la [Pantalla de validación](validation.md) y en la pantalla de Informe, si la estación a la que pertenecen está etiquetada como pública o interna.
