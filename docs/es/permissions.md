# Sistema de permisos

El sistema de permisos de Paricia está diseñado para permitir que los administradores de datos agreguen y validen nuevos datos, y que el público en general vea y recupere los datos publicados públicamente. Al mismo tiempo, garantiza la coherencia de los datos al evitar que los datos enviados se vuelvan huérfanos, por ejemplo, por la eliminación accidental de información clave de la que dependen.

Se aplican los siguientes principios:

- Los **usuarios anónimos** (usuarios no registrados) pueden ver datos en la herramienta de informes de estaciones que están etiquetadas como **públicas**. Estas estaciones también aparecen en el mapa de la página principal.
- Los **usuarios registrados** pueden:
- Ver datos de estaciones propiedad de otros usuarios y etiquetadas como **públicas** o **internas**, así como sus propios datos.
- Crear nuevos elementos, como formatos, sensores, estaciones, etc. Estos elementos pueden depender de otros objetos públicos u objetos privados propiedad del usuario.
- Cargar nuevos datos en estaciones para las que tienen permiso de `cambio` (esto incluye estaciones de su propiedad).
- Validar datos asociados a estaciones para las que tienen permiso de "cambio" (esto incluye estaciones de su propiedad).
- Los [**Usuarios administradores**](./admin.md) pueden:
- Administrar todos los datos y objetos, privados o públicos.
- Administrar usuarios.

!!! advertencia "Eliminación de objetos"

Los objetos en la base de datos **no se pueden eliminar si son utilizados por otros objetos**, independientemente de los permisos del usuario (incluso en el caso de usuarios administradores). Por ejemplo, si un formato particular usa cierto delimitador, ese objeto delimitador no se puede eliminar. Todos los objetos asociados deben eliminarse primero. Ver discusión [aquí](https://stackoverflow.com/a/48272690/3778792).

## Visibilidad de objetos

El atributo **visibilidad** de todos los objetos en la base de datos controla si el objeto puede ser visto por usuarios anónimos y referenciado por otros usuarios registrados en sus propios objetos. Al crear un nuevo objeto, los usuarios deben tener cuidado de seleccionar un nivel de visibilidad apropiado para su caso de uso (público o privado). Si el objeto es público, entonces puede ser referenciado por objetos de otros usuarios y por lo tanto no será posible eliminarlo, si fuera necesario en algún momento, ya que el propietario del objeto no tendrá acceso a los objetos asociados que hacen referencia a los suyos.

Las **estaciones** son un poco diferentes a otros objetos en el siguiente sentido:

- Para poder hacer referencia a ellas, un usuario debe tener permiso de `cambio` para esa estación. Hacerlas públicas no es suficiente, eso solo hace que sus datos estén disponibles públicamente.
- Tienen otro nivel de visibilidad, `interno`, que permite que los datos de la estación sean **visibles solo para usuarios registrados**.

La visibilidad de los nuevos objetos siempre es **privada** por defecto.

!!! advertencia "Permiso de `cambio` de estaciones"

Solo los usuarios administradores pueden dar permiso de `cambio` para una estación a otro usuario. Esto se hace a través de la página de administración de esa estación.