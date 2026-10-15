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
Pantallas: `/#/tareas` (lista), `/#/tareas/nueva` (formulario), `/#/tareas/{id}` (detalle).

- AC-1: En la pantalla `/#/tareas/nueva`, al escribir un título en el campo "Título" y pulsar el botón "Guardar tarea", se abre el detalle de la tarea con el mensaje "Tarea creada." y el estado "Pendiente".
- AC-2: En la pantalla `/#/tareas/nueva`, al pulsar "Guardar tarea" con el título vacío, aparece el mensaje de error "El título es obligatorio y admite hasta 100 caracteres." y no se crea la tarea.
- AC-3: En la pantalla `/#/tareas`, la tabla muestra cada tarea creada con su título y su estado.
- AC-4: Con una tarea creada antes desde `/#/tareas/nueva`, en la pantalla `/#/tareas`, al pulsar el botón "Completar" de una tarea, aparece el mensaje `Tarea "<título>" completada.` y su estado pasa a "Hecha".
- AC-5: Con una tarea creada antes desde `/#/tareas/nueva`, en la pantalla `/#/tareas`, al pulsar el botón "Eliminar" de una tarea, aparece el mensaje `Tarea "<título>" eliminada.` y la tarea deja de verse en la tabla.
- AC-6: Al abrir la pantalla `/#/tareas/99999`, aparece el mensaje "La tarea no existe.".
