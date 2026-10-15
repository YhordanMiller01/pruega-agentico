from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_crear_y_consultar_tarea():
    r = client.post("/tasks", json={"title": "Comprar pan"})
    assert r.status_code == 201
    tarea = r.json()
    assert tarea["title"] == "Comprar pan" and tarea["done"] is False
    assert client.get(f"/tasks/{tarea['id']}").json() == tarea


def test_titulo_vacio_se_rechaza():
    assert client.post("/tasks", json={"title": ""}).status_code == 422


def test_completar_tarea():
    tid = client.post("/tasks", json={"title": "Pagar luz"}).json()["id"]
    r = client.patch(f"/tasks/{tid}", json={"done": True})
    assert r.status_code == 200 and r.json()["done"] is True


def test_eliminar_tarea():
    tid = client.post("/tasks", json={"title": "Borrar"}).json()["id"]
    assert client.delete(f"/tasks/{tid}").status_code == 204
    assert client.get(f"/tasks/{tid}").status_code == 404


def test_tarea_inexistente():
    assert client.get("/tasks/99999").status_code == 404


# --- Criterios de aceptación de docs/historias.md que faltaban (HU-1 AC-3, HU-3 AC-2, HU-4 AC-2) ---


def test_titulo_de_100_caracteres_se_acepta_y_de_101_se_rechaza():
    assert client.post("/tasks", json={"title": "a" * 100}).status_code == 201
    assert client.post("/tasks", json={"title": "a" * 101}).status_code == 422


def test_completar_tarea_inexistente():
    assert client.patch("/tasks/99999", json={"done": True}).status_code == 404


def test_eliminar_tarea_inexistente():
    assert client.delete("/tasks/99999").status_code == 404


def test_patch_con_titulo_vacio_se_rechaza():
    tid = client.post("/tasks", json={"title": "Editar"}).json()["id"]
    assert client.patch(f"/tasks/{tid}", json={"title": ""}).status_code == 422


def test_el_contrato_declara_los_404():
    paths = app.openapi()["paths"]
    for method in ("get", "patch", "delete"):
        assert "404" in paths["/tasks/{task_id}"][method]["responses"]


def test_el_contrato_declara_servers():
    assert app.openapi()["servers"] == [{"url": "/"}]


# --- GUI (tasks-web) servida por la misma app; fuera del contrato ---
def test_gui_en_la_raiz_y_fuera_del_contrato():
    r = client.get("/")
    assert r.status_code == 200 and "text/html" in r.headers["content-type"]
    assert "/" not in app.openapi()["paths"]


# --- Login de demo para la identidad `ui` de sq_ai; fuera del contrato ---
def test_login_de_demo_devuelve_token():
    r = client.post("/auth/login", json={"email": "demo@pruega.local", "password": "demo1234"})
    assert r.status_code == 200 and r.json()["token"]


def test_login_con_credenciales_malas_responde_401():
    r = client.post("/auth/login", json={"email": "demo@pruega.local", "password": "x"})
    assert r.status_code == 401


def test_login_fuera_del_contrato_y_la_api_sigue_publica():
    assert "/auth/login" not in app.openapi()["paths"]
    assert len(app.openapi()["paths"]) == 3  # /health, /tasks, /tasks/{task_id}: 6 endpoints
    assert client.get("/tasks").status_code == 200  # sin token


# --- Semilla: la pantalla de lista arranca con filas ---
def test_la_lista_arranca_con_las_tareas_semilla():
    titulos = {t["title"] for t in client.get("/tasks").json()}
    assert {"Comprar pan", "Pagar la luz", "Llamar al médico"} <= titulos
    assert client.get("/tasks/99999").status_code == 404


def test_ruta_con_barra_final_no_existe():
    assert client.get("/tasks/", follow_redirects=False).status_code == 404
