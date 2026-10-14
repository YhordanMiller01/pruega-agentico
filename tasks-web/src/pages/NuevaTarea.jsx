import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { crearTarea } from "../api";

export default function NuevaTarea() {
  const [titulo, setTitulo] = useState("");
  const [error, setError] = useState("");
  const [enviando, setEnviando] = useState(false);
  const navegar = useNavigate();

  // Sin validación en el cliente: la regla (1..100 caracteres) la decide la API y la UI muestra su 422.
  const guardar = async (e) => {
    e.preventDefault();
    setError(""); setEnviando(true);
    try {
      const t = await crearTarea(titulo);
      navegar(`/tareas/${t.id}`, { state: { aviso: "Tarea creada." } });
    } catch (err) {
      setError(err.message);
    } finally {
      setEnviando(false);
    }
  };

  return (
    <section aria-labelledby="titulo-nueva">
      <h2 id="titulo-nueva">Nueva tarea</h2>
      <form onSubmit={guardar} noValidate>
        <label htmlFor="titulo">Título</label>
        <input id="titulo" name="titulo" value={titulo}
          onChange={(e) => setTitulo(e.target.value)} aria-invalid={Boolean(error)}
          aria-describedby={error ? "error-titulo" : undefined} />
        {error && <p id="error-titulo" role="alert" className="error">{error}</p>}
        <button type="submit" disabled={enviando} aria-busy={enviando}>Guardar tarea</button>
      </form>
    </section>
  );
}
