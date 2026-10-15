# pruega-agentico

Repositorio de prueba para el camino feliz de **sq_ai**: una API de tareas pequeña y en memoria, más una GUI web sobre ella, que sirven de sistema bajo prueba (SUT) para los agentes de API (F1.7) y de UI (F2.1).

```
pruega-agentico/
├── docs/historias.md      # 5 historias, 16 criterios de aceptación (HU-5 = pantallas)
├── docs/esperado.json     # resultado correcto esperado de cada agente de sq_ai
├── kustomization.yaml     # kubectl apply -k .  → despliega el SUT en el clúster
├── docker-compose.yml     # SUT en local (:4010)
├── tasks-api/             # servicio (carpeta de primer nivel = servicio para el escaneo de F0.1)
│   ├── app/main.py        # FastAPI, 6 endpoints + GUI en "/" y login de demo (fuera del contrato)
│   ├── app/static/        # GUI compilada (un solo index.html; la genera tasks-web)
│   ├── openapi.json       # contrato (generado desde la app)
│   ├── deploy-k8s.yaml    # Deployment + Service (namespace sqai-demo, imagen pública)
│   ├── Dockerfile         # imagen del SUT (puerto 4010)
│   ├── requirements.txt   # manifiesto del servicio, versiones fijadas
│   └── tests/             # 18 pruebas pytest
└── tasks-web/             # fuente de la GUI: Vite + React + React Router (HashRouter)
    └── src/App.jsx        # router: F0.1 saca de aquí el ui_map (/#/tareas, /#/tareas/nueva, /#/tareas/:id)
```

## GUI para F2.1

La API sirve la GUI en `/`: un solo servicio y una sola URL para F1.7 y F2.1. La GUI navega con `#`, así que no choca con `/tasks`.

- **Anónima**: sin login.
- **Accesible a propósito**, porque F2.1 localiza los elementos por rol y por nombre: los inputs tienen `<label>`, los botones tienen texto, los errores salen en `role="alert"`, los avisos en `role="status"` y la carga se marca con `aria-busy`.
- **Sin validación en el cliente**: los mensajes de 422 y 404 los provoca la API, así que la UI y la API no pueden contradecirse.
- **Un solo HTML con el JS inline**, porque el CSP del clúster no deja cargar scripts aparte.

Si cambias `tasks-web/src`, regenera la GUI y commitea `tasks-api/app/static/index.html`:

```bash
cd tasks-web && npm ci && npm run build    # escribe ../tasks-api/app/static/index.html
npm run dev                                # desarrollo en :5180 (con la API en :4010)
```

## Desplegar en el clúster

```bash
kubectl apply -k .     # namespace sqai-demo (el de demo-shop); el pod necesita salida a PyPI
```

Configuración del **proyecto** en sq_ai:

| Clave | Valor |
|---|---|
| URL de la API (F0.1/F1.7) | `http://tasks-demo.sqai-demo.svc.cluster.local:4010` |
| `ui_base_url` | `http://tasks-demo.sqai-demo.svc.cluster.local:4010/` |
| `ui_environment_type` | `qa` |
| `ui_allowed_egress` | `["tasks-demo.sqai-demo.svc.cluster.local"]` |

Sin `ui_base_url`, F2.1 omite todos los casos con `no_ui_target`.

### Identidad `ui` (sesión de F2.1)

La app es pública, pero F2.1 declara la corrida como **no autenticada** (`auth_required`, cobertura PARCIAL) si el proyecto no tiene identidad `ui`. Para eso la API trae un login de demo, `POST /auth/login`, fuera del contrato: con `{"email","password"}` correctos responde `{"token": "..."}` y F2.1 guarda ese token en `localStorage['token']` antes de navegar. Ningún endpoint exige el token.

| Dónde | Clave | Valor |
|---|---|---|
| `config_jsonb` del conector `openapi` | `auth_login_path` | `/auth/login` |
| Secreto del conector `openapi` | `ui_email` / `ui_password` | `demo@pruega.local` / `demo1234` (cámbialos con `DEMO_EMAIL` / `DEMO_PASSWORD`) |

Solo se declara la identidad `ui`: sin `email`/`password` en el secreto, F1.7 sigue llamando a la API sin login.

## Ejecutar la API

```bash
cd tasks-api
python -m venv .venv && . .venv/Scripts/activate   # en Linux/macOS: . .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q                      # 18 pruebas
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
