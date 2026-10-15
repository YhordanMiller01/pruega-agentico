import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate, useParams } from "react-router-dom";
import { obtenerTarea, completarTarea, eliminarTarea } from "../api";

export default function DetalleTarea() {
  const { id } = useParams();
  const { state } = useLocation();
  const navegar = useNavigate();
  // Igual que la lista: si la tarea viene en el HTML se pinta sin esperar al fetch.
  const [tarea, setTarea] = useState(
    () => (window.__TAREAS__ ?? []).find((t) => String(t.id) === id) ?? null);
  const [error, setError] = useState("");
  const [aviso, setAviso] = useState(state?.aviso ?? "");

  useEffect(() => {
    obtenerTarea(id).then(setTarea).catch((e) => setError(e.message));
  }, [id]);

  const completar = async () => {
    setError("");
    try {
      setTarea(await completarTarea(id));
      setAviso("Tarea completada.");
    } catch (e) { setError(e.message); }
  };

  const eliminar = async () => {
    setError("");
    try {
      await eliminarTarea(id);
      navegar("/tareas");
    } catch (e) { setError(e.message); }
  };

  return (
    <section aria-labelledby="titulo-detalle">
      <h2 id="titulo-detalle">Detalle de la tarea</h2>
      {aviso && <p role="status" className="aviso">{aviso}</p>}
      {error && <p role="alert" className="error">{error}</p>}
      {!tarea && !error && <p aria-busy="true">Cargando tarea…</p>}
      {tarea && (
        <>
          <dl>
            <dt>Número</dt><dd>{tarea.id}</dd>
            <dt>Título</dt><dd>{tarea.title}</dd>
            <dt>Estado</dt><dd>{tarea.done ? "Hecha" : "Pendiente"}</dd>
          </dl>
          <div className="acciones">
            <button type="button" disabled={tarea.done} onClick={completar}>Completar</button>
            <button type="button" className="peligro" onClick={eliminar}>Eliminar</button>
          </div>
        </>
      )}
      <p><Link to="/tareas">Volver a la lista</Link></p>
    </section>
  );
}
