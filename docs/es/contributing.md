<!-- markdownlint-disable MD033 -->
# Contribuir a Paricia

¡Gracias por tomarte el tiempo de contribuir a Paricia!

El siguiente es un conjunto de pautas para contribuir a Paricia, un proyecto de sistema de gestión de datos hidroclimáticos basado en Python. El objetivo de estas pautas es hacer que el desarrollo del proyecto sea eficiente y sostenible y garantizar que cada envío lo haga mejor, más legible, más sólido y mejor documentado. No dudes en sugerir cambios y mejoras.

## Índice

[Código de conducta](#code-of-conduct)

[¿Cómo puedo contribuir?](#how-can-i-contribute)

- [Informar errores](#reporting-bugs)
- [Sugerir mejoras](#suggesting-enhancements)
- [Tu primera contribución de código](#your-first-code-contribution)
- [Solicitudes de incorporación de cambios](#pull-requests)

[Guías de estilo](#styleguides)

- [Mensajes de confirmación de Git](#git-commit-messages)
- [Guía de estilo de la documentación](#documentation-styleguide)

## Código de conducta

Este proyecto y todos los participantes en él se rigen por el [Código de conducta de Paricia](CODE_OF_CONDUCT.md). Al participar, se espera que respetes este código. Por favor, informe cualquier comportamiento inaceptable al [Administrador del repositorio](https://www.imperial.ac.uk/people/w.buytaert).

## ¿Cómo puedo contribuir?

### Informar errores

Esta sección le guía a través del envío de un informe de error para Paricia. Seguir estas pautas ayuda a los encargados del mantenimiento y a la comunidad a:

- :pencil: comprender su informe
- :computer: reproducir el comportamiento
- :mag_right: encontrar informes relacionados

Antes de crear informes de error, consulte [esta lista](https://github.com/ImperialCollegeLondon/paricia/issues) (incluidos los problemas cerrados) ya que puede descubrir que no necesita crear uno. Cuando esté creando un informe de error, [incluya tantos detalles como sea posible](#cómo-envío-un-buen-informe-de-error).

> **Nota:** Si encuentra un problema **Cerrado** que parece ser lo mismo que está experimentando, abra un nuevo problema e incluya un enlace al problema original en el cuerpo del nuevo.

#### ¿Cómo envío un (buen) informe de error?

Los errores se registran como [problemas de GitHub](https://guides.github.com/features/issues/). Explique el problema e incluya detalles adicionales para ayudar a los encargados de mantenimiento a reproducirlo:

- **Use un título claro y descriptivo** para el problema para identificarlo.
- **Describe los pasos exactos que reproducen el problema** con tantos detalles como sea posible. Por ejemplo, comience explicando cómo instaló Paricia y qué estaba tratando de hacer.
- **Proporcione ejemplos específicos para demostrar los pasos**. Incluya enlaces a archivos o proyectos de GitHub, o fragmentos que se puedan copiar y pegar, que use en esos ejemplos. Si proporciona fragmentos en el problema, utilice [bloques de código Markdown](https://help.github.com/articles/markdown-basics/#multiple-lines).
- **Describe el comportamiento que observaste después de seguir los pasos** y señala cuál es exactamente el problema con ese comportamiento.
- **Explica qué comportamiento esperabas ver en su lugar y por qué.**
- **Si hay algún resultado de error en la terminal, incluye ese resultado en tu informe.**

Proporciona más contexto respondiendo estas preguntas:

- **¿El problema comenzó a ocurrir recientemente** (por ejemplo, después de actualizar a una nueva versión de Paricia) o siempre fue un problema?
- Si el problema comenzó a ocurrir recientemente, **¿puedes reproducir el problema en una versión anterior de Paricia?** ¿Cuál es la versión más reciente en la que no ocurre el problema? Puedes descargar versiones anteriores de Paricia desde [la página de versiones](https://github.com/ImperialCollegeLondon/paricia/releases).
- **¿Puedes reproducir el problema de manera confiable?** Si no, proporciona detalles sobre la frecuencia con la que ocurre el problema y bajo qué condiciones ocurre normalmente.

Incluye detalles sobre tu configuración y entorno:

- **¿Qué versión de Paricia estás usando?**
- **¿Cuál es el nombre y la versión del sistema operativo que estás usando**?
- **¿Estás ejecutando Paricia en una máquina virtual?** Si es así, ¿qué software de VM estás usando y qué sistemas operativos y versiones se usan para el host y el invitado?

### Sugerencias de mejoras

Esta sección te guía a través del envío de una sugerencia de mejora para Paricia, incluidas características completamente nuevas y mejoras menores a la funcionalidad existente. Seguir estas pautas ayuda a los encargados del mantenimiento y a la comunidad a comprender tu sugerencia y encontrar otras relacionadas.

Antes de crear sugerencias de mejora, consulta [esta lista](https://github.com/ImperialCollegeLondon/paricia/issues) (incluidos los problemas cerrados), ya que es posible que descubras que no necesitas crear una. Cuando cree una sugerencia de mejora, incluya tantos detalles como sea posible (#¿Cómo envío una buena sugerencia de mejora?).

#### ¿Cómo envío una buena sugerencia de mejora?

Las sugerencias de mejora se registran como [problemas de GitHub](https://guides.github.com/features/issues/). Cree un problema en ese repositorio y proporcione la siguiente información:

### Tu primera contribución de código

¿No estás seguro de por dónde empezar a contribuir con Paricia? Puedes empezar por revisar estos problemas para principiantes y para quienes necesitan ayuda:

- [Problemas para principiantes](https://github.com/ImperialCollegeLondon/paricia/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22): problemas que solo deberían requerir unas pocas líneas de código y una o dos pruebas.
- [Problemas para quienes necesitan ayuda](https://github.com/ImperialCollegeLondon/paricia/labels/help%20wanted): problemas que deberían ser un poco más complejos que los problemas para principiantes.

### Pull Requests

El proceso que se describe aquí tiene varios objetivos:

- Mantener la calidad de Paricia
- Solucionar problemas que son importantes para los usuarios
- Involucrar a la comunidad en el trabajo para lograr la mejor Paricia posible
- Permitir un sistema sostenible para que los encargados de mantenimiento de Paricia revisen las contribuciones

Siga estos pasos para que los encargados de mantenimiento consideren su contribución:

1. **Describa claramente cuál es el propósito de la pull request**. Consulte los problemas relevantes en [Errores](#reporting-bugs) o [Mejoras](#suggesting-enhancements). En general, un problema siempre debe abrirse *antes* de una pull request, para discutir su contenido con un encargado de mantenimiento y asegurarse de que tenga sentido para Paricia. Si la pull request es un trabajo en progreso que llevará algún tiempo para estar listo pero aún así desea discutirlo con la comunidad, abra un [borrador de pull request](https://github.blog/2019-02-14-introducing-draft-pull-requests/).
2. **Incluya pruebas unitarias y pruebas de integración relevantes, cuando sea necesario**. El conjunto de pruebas de Paricia es bastante limitado en este momento. Estamos trabajando para mejorar esto y probar tantas características como sea posible, por lo que cualquier nueva incorporación al código debe venir con su propio conjunto de pruebas para evitar retroceder en este asunto.
3. **Para nuevas características y mejoras, incluya documentación y ejemplos**. Tanto en el código, como cadenas de documentación en clases, funciones y módulos, y como documentación adecuada que describa cómo usar la nueva característica.
4. Siga las [guías de estilo](#styleguides)
5. Después de enviar su solicitud de extracción, verifique que todas las [verificaciones de estado](https://help.github.com/articles/about-status-checks/) estén pasando <details><summary>¿Qué pasa si las verificaciones de estado fallan?</summary>Si una verificación de estado falla y cree que el error no está relacionado con su cambio, deje un comentario en la solicitud de extracción explicando por qué cree que el error no está relacionado. Un encargado de mantenimiento volverá a ejecutar la verificación de estado por usted. Si concluimos que el error fue un falso positivo, abriremos un problema para rastrear ese problema con nuestro conjunto de verificación de estado.

Si bien los requisitos previos anteriores deben cumplirse antes de que se revise su solicitud de incorporación de cambios, el revisor o los revisores pueden solicitarle que complete trabajo de diseño adicional, pruebas u otros cambios antes de que su solicitud de incorporación de cambios pueda ser finalmente aceptada.

## Guías de estilo

### Mensajes de confirmación de Git

- Use el tiempo presente ("Agregar característica" no "Característica agregada")
- Use el modo imperativo ("Mover el cursor a..." no "Mueve el cursor a...")
- Limite la primera línea a 72 caracteres o menos
- Haga referencia a problemas y solicitudes de incorporación de cambios generosamente después de la primera línea
- Cuando solo cambie la documentación, incluya `[ci skip]` en el título de la confirmación
- Considere comenzar el mensaje de confirmación con un emoji aplicable:
- :art: `:art:` cuando mejore el formato/estructura del código
- :racehorse: `:racehorse:` cuando mejore el rendimiento
- :non-potable_water: `:non-potable_water:` cuando solucione fugas de memoria
- :memo: `:memo:` cuando escriba documentación
- :penguin: `:penguin:` cuando arregle algo en Linux
- :apple: `:apple:` cuando arregle algo en macOS
- :checkered_flag: `:checkered_flag:` al reparar algo en Windows
- :bug: `:bug:` al reparar un error
- :fire: `:fire:` al eliminar código o archivos
- :green_heart: `:green_heart:` al reparar la compilación de CI
- :white_check_mark: `:white_check_mark:` al agregar pruebas
- :lock: `:lock:` al lidiar con la seguridad
- :arrow_up: `:arrow_up:` al actualizar dependencias
- :arrow_down: `:arrow_down:` al degradar dependencias
- :shirt: `:shirt:` al eliminar advertencias de linter

### Guía de estilo de la documentación

- Use [Markdown](https://daringfireball.net/projects/markdown).
- Métodos y clases de referencia en Markdown con la notación personalizada `{}`:
- Clases de referencia con `{ClassName}`
- Métodos de instancia de referencia con `{ClassName::methodName}`
- Métodos de clase de referencia con `{ClassName.methodName}`