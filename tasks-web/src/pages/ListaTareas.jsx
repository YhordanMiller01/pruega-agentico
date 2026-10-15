import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { listarTareas, completarTarea, eliminarTarea } from "../api";

export default function ListaTareas() {
  const [tareas, setTareas] = useState(null);
  const [error, setError] = useState("");
  const [aviso, setAviso] = useState("");

  const cargar = () =>
    listarTareas().then(setTareas).catch((e) => setError(e.message));

  useEffect(() => { cargar(); }, []);

  const completar = async (t) => {
    setError(""); setAviso("");
    try {
      await completarTarea(t.id);
      setAviso(`Tarea "${t.title}" completada.`);
      cargar();
    } catch (e) { setError(e.message); }
  };

  const eliminar = async (t) => {
    setError(""); setAviso("");
    try {
      await eliminarTarea(t.id);
      setAviso(`Tarea "${t.title}" eliminada.`);
      cargar();
    } catch (e) { setError(e.message); }
  };

  return (
    <section aria-labelledby="titulo-lista">
      <h2 id="titulo-lista">Lista de tareas</h2>
      {aviso && <p role="status" className="aviso">{aviso}</p>}
      {error && <p role="alert" className="error">{error}</p>}
      {tareas === null ? (
        <p aria-busy="true">Cargando tareas…</p>
      ) : tareas.length === 0 ? (
        <p>No tienes tareas. <Link to="/tareas/nueva">Crear la primera</Link></p>
      ) : (
        <table>
          <thead>
            <tr><th scope="col">Título</th><th scope="col">Estado</th><th scope="col">Acciones</th></tr>
          </thead>
          <tbody>
            {tareas.map((t) => (
              <tr key={t.id}>
                <td><Link to={`/tareas/${t.id}`}>{t.title}</Link></td>
                <td>{t.done ? "Hecha" : "Pendiente"}</td>
                <td className="acciones">
                  <button type="button" disabled={t.done} onClick={() => completar(t)}
                    aria-label={`Completar ${t.title}`}>Completar</button>
                  <button type="button" className="peligro" onClick={() => eliminar(t)}
                    aria-label={`Eliminar ${t.title}`}>Eliminar</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}
