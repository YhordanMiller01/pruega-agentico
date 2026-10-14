# Historias de usuario: Tasks API

Fuente de requisitos para el ciclo de QA. Cada criterio de aceptación (AC) es verificable contra la API.

## HU-1: Crear una tarea
Como usuario quiero crear una tarea con un título para llevar mi lista de pendientes.

- AC-1: `POST /tasks` con un título válido responde `201` y devuelve la tarea con `id`, `title` y `done=false`.
- AC-2: `POST /tasks` con el título vacío responde `422`.
- AC-3: El título admite hasta 100 caracteres; con más responde `422`.

## HU-2: Consultar mis tareas
Como usuario quiero ver mis tareas para saber qué tengo pendiente.

- AC-1: `GET /tasks` responde `200` con la lista de tareas.
- AC-2: `GET /tasks/{id}` responde `200` con la tarea si existe.
- AC-3: `GET /tasks/{id}` responde `404` si la tarea no existe.

## HU-3: Completar una tarea
Como usuario quiero marcar una tarea como hecha para llevar el avance.

- AC-1: `PATCH /tasks/{id}` con `done=true` responde `200` y la tarea queda con `done=true`.
- AC-2: `PATCH /tasks/{id}` sobre una tarea inexistente responde `404`.

## HU-4: Eliminar una tarea
Como usuario quiero eliminar una tarea que ya no necesito.

- AC-1: `DELETE /tasks/{id}` responde `204` y la tarea deja de existir.
- AC-2: `DELETE /tasks/{id}` sobre una tarea inexistente responde `404`.
