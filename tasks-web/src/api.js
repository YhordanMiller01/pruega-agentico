// Mismo origen: nginx (contenedor) o Vite (local) reenvían /api/* a tasks-api.
const BASE = "/api";

async function pedir(ruta, opciones = {}) {
  const r = await fetch(BASE + ruta, {
    headers: { "Content-Type": "application/json" },
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
