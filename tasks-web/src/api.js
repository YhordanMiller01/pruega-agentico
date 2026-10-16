// Mismo origen: tasks-api sirve esta GUI en "/" y la API en /tasks (en local, Vite reenvía).
const BASE = "";

async function pedir(ruta, opciones = {}) {
  const r = await fetch(BASE + ruta, {
    // X-Origen: la API distingue las altas hechas desde la GUI (modo deriva, AB#3068).
    headers: { "Content-Type": "application/json", "X-Origen": "gui" },
    ...opciones,
  });
  if (r.status === 204) return null;
  const cuerpo = await r.json().catch(() => null);
  if (!r.ok) {
    const error = new Error(mensajeDeError(r.status));
    error.status = r.status;
    throw error;
  }
  return cuerpo;
}

function mensajeDeError(status) {
  if (status === 404) return "La tarea no existe.";
  if (status === 422) return "El título es obligatorio y admite hasta 100 caracteres.";
  return "No se pudo completar la operación.";
}

export const listarTareas = () => pedir("/tasks");
export const obtenerTarea = (id) => pedir(`/tasks/${id}`);
export const crearTarea = (title) => pedir("/tasks", { method: "POST", body: JSON.stringify({ title }) });
export const completarTarea = (id) => pedir(`/tasks/${id}`, { method: "PATCH", body: JSON.stringify({ done: true }) });
export const eliminarTarea = (id) => pedir(`/tasks/${id}`, { method: "DELETE" });
