import { HashRouter, Routes, Route, Navigate, NavLink } from "react-router-dom";
import ListaTareas from "./pages/ListaTareas";
import NuevaTarea from "./pages/NuevaTarea";
import DetalleTarea from "./pages/DetalleTarea";

// HashRouter: F0.1 lee este router y publica las pantallas como /#/<ruta> (ui_map).
export default function App() {
  return (
    <HashRouter>
      <header className="cabecera">
        <h1>Mis tareas</h1>
        <nav aria-label="Principal">
          <NavLink to="/tareas" end>Lista de tareas</NavLink>
          <NavLink to="/tareas/nueva">Nueva tarea</NavLink>
        </nav>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Navigate to="/tareas" replace />} />
          <Route path="/tareas" element={<ListaTareas />} />
          <Route path="/tareas/nueva" element={<NuevaTarea />} />
          <Route path="/tareas/:id" element={<DetalleTarea />} />
          <Route path="*" element={<Navigate to="/tareas" replace />} />
        </Routes>
      </main>
    </HashRouter>
  );
}
