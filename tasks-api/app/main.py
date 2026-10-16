"""API de tareas en memoria: sistema bajo prueba (SUT) para el camino feliz de sq_ai."""
import json
import os
import secrets
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

# `servers` declara la base de las peticiones; sin él, sq_ai usa la URL del propio openapi.json.
app = FastAPI(title="Tasks API", version="1.0.0", servers=[{"url": "/"}],
              redirect_slashes=False)  # /tasks/ es una ruta inexistente: 404, no redirección

_NOT_FOUND = {404: {"description": "Task not found"}}

# Semilla: la lista arranca con tareas para que la pantalla /#/tareas tenga filas y botones
# (Completar/Eliminar) que F2.1 pueda ver; sin ella su inventario salía vacío. SEED_TASKS=0
# la desactiva.
_SEMILLA = ["Comprar pan", "Pagar la luz", "Llamar al médico"]
_CON_SEMILLA = os.environ.get("SEED_TASKS", "1") != "0"
_tasks: dict[int, dict] = {}


def _restaurar_semilla() -> None:
    # Las tareas semilla vuelven a su estado inicial (Pendiente, título original). Sin esto,
    # el primer caso de HU-5/AC-4 deja "Pagar la luz" en Hecha (botón Completar deshabilitado)
    # y el de AC-5 borra "Llamar al médico": el re-run de F2.1, el siguiente ciclo o cualquier
    # PATCH/DELETE de F1.7 sobre los ids 1-3 hacían fallar esos casos sin defecto del SUT.
    for i, t in enumerate(_SEMILLA, start=1):
        _tasks[i] = {"id": i, "title": t, "done": False}


if _CON_SEMILLA:
    _restaurar_semilla()
_next_id = len(_tasks) + 1


class TaskIn(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    done: bool = False


class TaskPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    done: bool | None = None


class Task(BaseModel):
    id: int
    title: str
    done: bool


# GUI de tasks-web (un solo HTML, `npm run build` en tasks-web). Fuera del contrato: el
# OpenAPI sigue con 6 endpoints. Navega con HashRouter, así que no choca con /tasks.
_GUI = Path(__file__).parent / "static" / "index.html"


# Modo deriva (para probar el self-healing de F2.1, AB#3068). Apagado por defecto: se activa
# con SUT_DERIVA_UI=1 o con POST /__deriva {"activa": true}. Activado, la primera alta de
# tarea hecha DESDE LA GUI (cabecera X-Origen: gui) renombra el botón «Guardar tarea» a
# «Guardar la tarea»: los casos planificados con el rótulo viejo fallan al ejecutar y el
# healing tiene que encontrar el nuevo. Las altas por API (F1.7) no lo disparan, y la captura
# de DOM de F2.1 no crea tareas, así que el plan siempre ve el rótulo original.
_ROTULO_GUARDAR = "Guardar tarea"
_ROTULO_GUARDAR_DERIVADO = "Guardar la tarea"
_deriva = {"activa": os.environ.get("SUT_DERIVA_UI", "0") == "1", "derivada": False}


class DerivaIn(BaseModel):
    activa: bool


@app.post("/__deriva", include_in_schema=False)
def deriva(body: DerivaIn) -> dict:
    """Activa o apaga el modo deriva y devuelve el rótulo al original."""
    _deriva.update(activa=body.activa, derivada=False)
    return dict(_deriva)


@app.get("/", include_in_schema=False)
def gui() -> HTMLResponse:
    # Las tareas actuales viajan en el HTML (window.__TAREAS__) para que la lista se pinte sin
    # esperar al fetch: F2.1 captura su inventario al cargar y antes la tabla aún no existía.
    # Cada caso de F2.1 abre la GUI desde cero: aquí la semilla vuelve a su estado inicial
    # para que los casos de HU-5 no dependan del orden ni de corridas anteriores.
    if _CON_SEMILLA:
        _restaurar_semilla()
    datos = json.dumps(list(_tasks.values()), ensure_ascii=False).replace("</", "<\\/")
    rotulo = _ROTULO_GUARDAR_DERIVADO if _deriva["derivada"] else _ROTULO_GUARDAR
    html = _GUI.read_text(encoding="utf-8").replace(
        "</head>", f"<script>window.__TAREAS__={datos};"
                   f"window.__ROTULO_GUARDAR__={json.dumps(rotulo, ensure_ascii=False)};"
                   "</script></head>", 1)
    return HTMLResponse(html)


# Login de demo para la identidad `ui` de sq_ai (F2.1): devuelve un token que F2.1 guarda en
# localStorage['token'] antes de navegar. La API y la GUI siguen siendo públicas —el token no
# se exige en ningún endpoint—; existe para que la corrida de UI se declare autenticada.
# Fuera del contrato: el OpenAPI sigue con 6 endpoints.
_DEMO_EMAIL = os.environ.get("DEMO_EMAIL", "demo@pruega.local")
_DEMO_PASSWORD = os.environ.get("DEMO_PASSWORD", "demo1234")


class LoginIn(BaseModel):
    email: str
    password: str


@app.post("/auth/login", include_in_schema=False)
def login(body: LoginIn) -> dict:
    if body.email != _DEMO_EMAIL or body.password != _DEMO_PASSWORD:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return {"token": secrets.token_urlsafe(24)}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[dict]:
    return list(_tasks.values())


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(body: TaskIn, request: Request) -> dict:
    global _next_id
    task = {"id": _next_id, **body.model_dump()}
    _tasks[_next_id] = task
    _next_id += 1
    # Modo deriva: solo un alta hecha desde la GUI renombra el botón (ver `_deriva`).
    if _deriva["activa"] and request.headers.get("x-origen") == "gui":
        _deriva["derivada"] = True
    return task


@app.get("/tasks/{task_id}", response_model=Task, responses=_NOT_FOUND)
def get_task(task_id: int) -> dict:
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return _tasks[task_id]


@app.patch("/tasks/{task_id}", response_model=Task, responses=_NOT_FOUND)
def update_task(task_id: int, body: TaskPatch) -> dict:
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    cambios = body.model_dump(exclude_none=True)
    if not cambios:  # PATCH sin campos: nada que actualizar, es un cuerpo inválido
        raise HTTPException(status_code=422, detail="Indica al menos title o done")
    _tasks[task_id].update(cambios)
    return _tasks[task_id]


@app.delete("/tasks/{task_id}", status_code=204, responses=_NOT_FOUND)
def delete_task(task_id: int) -> Response:
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del _tasks[task_id]
    return Response(status_code=204)
