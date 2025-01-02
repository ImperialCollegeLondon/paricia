# Añadir elementos

Los usuarios registrados pueden utilizar elementos existentes (formatos, variables, etc.) siempre que sean públicos (consulte la sección [Permisos](./permissions.md)), pero también pueden crear elementos suyos propios para satisfacer sus necesidades específicas.

Todos los elementos que se pueden crear en Paricia (excepto la importación de datos, que se analiza en [su propia sección](./importing_data.md)) siguen un flujo de trabajo similar:

- Seleccione el elemento de interés en el submenú de la barra superior, por ejemplo, `Variable` dentro del menú `Variables`.

![Selección de un elemento en el menú superior](../assets/images/selecting_component.png)

- La página ahora muestra la lista de elementos existentes de ese tipo que el usuario puede ver, es decir, los que son públicos o los que son propios. Puede ordenar las entradas haciendo clic en los nombres de las columnas o filtrarlas para seleccionar solo algunas entradas.

![Lista de variables que un usuario puede ver](../assets/images/variables_list.png)

- Al hacer clic en el ID de un elemento existente, puede ver los detalles de ese elemento y editarlo, si el usuario tiene permiso para hacerlo.
- Al hacer clic en el botón `Nuevo` en la parte superior, puede crear un nuevo elemento de ese tipo.

Se abrirá un nuevo formulario con los campos que deben completarse para ese elemento.

Algunos elementos son muy simples y solo tienen uno o dos campos para completar. Otros son más complicados y vinculan, a su vez, a otros elementos. No todos los campos son obligatorios, en general. Si un campo obligatorio no se completa, se marcará al intentar guardar el elemento.

Tomemos como ejemplo el formulario de creación de variables.

![Formulario utilizado para crear una nueva variable](../assets/images/variable_creation.png)

Como podemos ver en este formulario, hay un campo llamado `Visibilidad`. Todos los elementos tienen este campo y define quién más puede ver los detalles y usar el elemento para definir sus propios elementos.

Otros campos, como `Unidad`, son claves externas a otros elementos y, en este caso, son solo informativos - metadatos para comprender mejor la variable.

Finalmente, algunos campos se utilizan durante el proceso de validación o importación. Ese es el caso del error máximo, mínimo o de diferencia, en este caso, que ayuda a Paricia a identificar y marcar entradas sospechosas.

Al crear un nuevo elemento, es importante que se comprenda correctamente el significado y el propósito de los campos. Todos ellos deben tener una descripción debajo explicando para qué sirven, pero si dicha información no está completa o clara, por favor repórtelo siguiendo las instrucciones de las [Pautas de contribución](./contributing.md).