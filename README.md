# pruega-agentico

Repositorio de prueba para el camino feliz de **sq_ai**: una API de tareas pequeña y en memoria, más una GUI web sobre ella, que sirven de sistema bajo prueba (SUT) para los agentes de API (F1.7) y de UI (F2.1).

```
pruega-agentico/
├── docs/historias.md      # 5 historias, 16 criterios de aceptación (HU-5 = pantallas)
├── docs/esperado.json     # resultado correcto esperado de cada agente de sq_ai
├── docker-compose.yml     # API (:4010) + GUI (:8081) en local
├── tasks-api/             # servicio (carpeta de primer nivel = servicio para el escaneo de F0.1)
│   ├── app/main.py        # FastAPI, 6 endpoints
│   ├── openapi.json       # contrato (generado desde la app)
│   ├── Dockerfile         # imagen del SUT (puerto 4010)
│   ├── requirements.txt   # manifiesto del servicio, versiones fijadas
│   └── tests/             # 12 pruebas pytest
└── tasks-web/             # GUI: Vite + React + React Router (HashRouter)
    ├── src/App.jsx        # router: F0.1 saca de aquí el ui_map (/#/tareas, /#/tareas/nueva, /#/tareas/:id)
    ├── nginx.conf.template# sirve la GUI y reenvía /api/* a tasks-api (API_UPSTREAM)
    └── Dockerfile         # imagen de la GUI (puerto 8080)
```

## GUI para F2.1

- **Anónima**: sin login.
- **Accesible a propósito**, porque F2.1 localiza los elementos por rol y por nombre: los inputs tienen `<label>`, los botones tienen texto, los errores salen en `role="alert"`, los avisos en `role="status"` y la carga se marca con `aria-busy`.
- **Sin validación en el cliente**: los mensajes de 422 y 404 los provoca la API, así que la UI y la API no pueden contradecirse.

```bash
docker compose up --build                  # GUI en http://localhost:8081, API en :4010
# o sin Docker:
cd tasks-web && npm ci && npm run dev      # GUI en :5180 (con la API en :4010)
```

Para que F2.1 ejecute, hay que configurar en el **proyecto** de sq_ai:

| Clave | Valor |
|---|---|
| `ui_base_url` | URL de `tasks-web` alcanzable desde el clúster (p. ej. `http://tasks-web.<ns>.svc.cluster.local:8080/`) |
| `ui_environment_type` | `qa` |
| `ui_allowed_egress` | `["<host de tasks-web>"]` |

Sin `ui_base_url`, F2.1 omite todos los casos con `no_ui_target`.

## Ejecutar la API

```bash
cd tasks-api
python -m venv .venv && . .venv/Scripts/activate   # en Linux/macOS: . .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q                      # 12 pruebas
python -m uvicorn app.main:app --port 4010
```

Contrato en `http://localhost:4010/openapi.json`.

## Endpoints

| Método | Ruta | Respuestas |
|---|---|---|
| GET | `/health` | 200 |
| GET | `/tasks` | 200 |
| POST | `/tasks` | 201, 422 |
| GET | `/tasks/{id}` | 200, 404, 422 (id no numérico) |
| PATCH | `/tasks/{id}` | 200, 404, 422 |
| DELETE | `/tasks/{id}` | 204, 404, 422 (id no numérico) |

## Regenerar `openapi.json`

```bash
cd tasks-api
python -c "import json; from app.main import app; open('openapi.json','w',encoding='utf-8').write(json.dumps(app.openapi(), indent=2, ensure_ascii=False)+'\n')"
```
