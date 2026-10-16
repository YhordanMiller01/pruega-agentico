# Historias de usuario: Tasks API

Fuente de requisitos para el ciclo de QA. Cada criterio de aceptación (AC) es verificable contra la API.

## HU-1: Crear una tarea
Como usuario quiero crear una tarea con un título para llevar mi lista de pendientes.
Acceso: público, sin inicio de sesión, sin token ni usuario; cualquier visitante anónimo puede usarla. Los errores de validación responden siempre `422` (nunca `400`).

- AC-1: `POST /tasks` con un título válido responde `201` y devuelve la tarea con `id`, `title` y `done=false`.
- AC-2: `POST /tasks` con el título vacío responde `422` (no `400`).
- AC-3: El título admite hasta 100 caracteres; con más responde `422`.

## HU-2: Consultar mis tareas
Como usuario quiero ver mis tareas para saber qué tengo pendiente.
Acceso: público, sin inicio de sesión, sin token ni usuario; cualquier visitante anónimo puede usarla. Los errores de validación responden siempre `422` (nunca `400`).

- AC-1: `GET /tasks` responde `200` con la lista de tareas.
- AC-2: `GET /tasks/{id}` responde `200` con la tarea si existe.
- AC-3: `GET /tasks/{id}` responde `404` si la tarea no existe.

## HU-3: Completar una tarea
Como usuario quiero marcar una tarea como hecha para llevar el avance.
Acceso: público, sin inicio de sesión, sin token ni usuario; cualquier visitante anónimo puede usarla. Los errores de validación responden siempre `422` (nunca `400`).

- AC-1: `PATCH /tasks/{id}` con `done=true` responde `200` y la tarea queda con `done=true`.
- AC-2: `PATCH /tasks/{id}` sobre una tarea inexistente responde `404`.

## HU-4: Eliminar una tarea
Como usuario quiero eliminar una tarea que ya no necesito.
Acceso: público, sin inicio de sesión, sin token ni usuario; cualquier visitante anónimo puede usarla. Los errores de validación responden siempre `422` (nunca `400`).

- AC-1: `DELETE /tasks/{id}` responde `204` y la tarea deja de existir.
- AC-2: `DELETE /tasks/{id}` sobre una tarea inexistente responde `404`.

## HU-5: Gestionar mis tareas desde la pantalla
Como usuario quiero manejar mis tareas desde la interfaz web, sin llamar a la API.
Acceso: público, sin inicio de sesión, sin token ni usuario; cualquier visitante anónimo puede usarla. La interfaz se abre directamente en la pantalla indicada, sin pantalla de login.
La lista arranca con tres tareas precargadas: "Comprar pan", "Pagar la luz" y "Llamar al médico", todas en estado "Pendiente".
Pantallas: `/#/tareas` (título "Lista de tareas"), `/#/tareas/nueva` (título "Nueva tarea"), `/#/tareas/{id}` (título "Detalle de la tarea"). El menú tiene los enlaces "Ver lista" y "Agregar tarea".

- AC-1: En la pantalla `/#/tareas/nueva`, al escribir un título en el campo "Título" y pulsar el botón "Guardar tarea", se abre el detalle de la tarea con el mensaje "Tarea creada." y el estado "Pendiente".
- AC-2: En la pantalla `/#/tareas/nueva`, al pulsar "Guardar tarea" con el título vacío, aparece el mensaje de error "El título es obligatorio y admite hasta 100 caracteres." y no se crea la tarea.
- AC-3: En la pantalla `/#/tareas`, la tabla muestra la fila "Comprar pan" con el estado "Pendiente".
- AC-4: En la pantalla `/#/tareas`, al pulsar el botón "Completar Pagar la luz", aparece el mensaje "Tarea completada: Pagar la luz." y su estado pasa a "Hecha".
- AC-5: En la pantalla `/#/tareas`, al pulsar el botón "Eliminar Llamar al médico", aparece el mensaje "Tarea eliminada: Llamar al médico." y esa fila deja de verse en la tabla.
- AC-6: Al abrir la pantalla `/#/tareas/99999`, aparece el mensaje "La tarea no existe.".

## HU-6: Lo que la lista de tareas no ofrece
Como usuario quiero que la lista solo ofrezca las acciones que existen, para no borrar todo por error.
Acceso: público, sin inicio de sesión, sin token ni usuario; cualquier visitante anónimo puede usarla. La interfaz se abre directamente en la pantalla indicada, sin pantalla de login.

- AC-1: En la pantalla `/#/tareas` no aparece ningún botón para vaciar toda la lista de tareas de una vez.
- AC-2: En la pantalla `/#/tareas`, después de pulsar el botón "Eliminar Llamar al médico", la fila "Llamar al médico" deja de verse en la tabla.

## HU-7: Buscar y filtrar mis tareas en la pantalla
Como usuario quiero buscar y filtrar la lista para encontrar rápido una tarea.
Acceso: público, sin inicio de sesión, sin token ni usuario; cualquier visitante anónimo puede usarla. La interfaz se abre directamente en la pantalla indicada, sin pantalla de login.
La lista arranca con tres tareas precargadas: "Comprar pan", "Pagar la luz" y "Llamar al médico", todas en estado "Pendiente".

- AC-1: En la pantalla `/#/tareas`, al escribir "pan" en el campo "Buscar tarea", la tabla muestra la fila "Comprar pan" y la fila "Pagar la luz" deja de verse.
- AC-2: En la pantalla `/#/tareas`, al escribir "zzz" en el campo "Buscar tarea", aparece el mensaje "Ninguna tarea coincide con la búsqueda.".
- AC-3: En la pantalla `/#/tareas`, después de pulsar el botón "Completar Pagar la luz" y marcar la casilla "Ocultar completadas", la fila "Pagar la luz" deja de verse y la fila "Comprar pan" sigue visible.
