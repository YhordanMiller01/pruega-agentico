"""API de tareas en memoria: sistema bajo prueba (SUT) para el camino feliz de sq_ai."""
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

# `servers` declara la base de las peticiones; sin él, sq_ai usa la URL del propio openapi.json.
app = FastAPI(title="Tasks API", version="1.0.0", servers=[{"url": "/"}])

_NOT_FOUND = {404: {"description": "Task not found"}}

_tasks: dict[int, dict] = {}
_next_id = 1


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


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[dict]:
    return list(_tasks.values())


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(body: TaskIn) -> dict:
    global _next_id
    task = {"id": _next_id, **body.model_dump()}
    _tasks[_next_id] = task
    _next_id += 1
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
    _tasks[task_id].update(body.model_dump(exclude_none=True))
    return _tasks[task_id]


@app.delete("/tasks/{task_id}", status_code=204, responses=_NOT_FOUND)
def delete_task(task_id: int) -> Response:
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del _tasks[task_id]
    return Response(status_code=204)
