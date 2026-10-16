#!/usr/bin/env bash
# Set de pruebas de humo contra la API levantada (por defecto http://localhost:4010).
# Uso: bash pruebas_endpoints.sh [BASE_URL]
BASE="${1:-http://localhost:4010}"
OK=0; FAIL=0

check() {  # check <descripción> <código esperado> <método> <ruta> [json]
  local desc="$1" esperado="$2" metodo="$3" ruta="$4" body="$5" code
  if [ -n "$body" ]; then
    code=$(curl -s -o /tmp/resp.json -w '%{http_code}' -X "$metodo" "$BASE$ruta" \
      -H 'Content-Type: application/json' -d "$body")
  else
    code=$(curl -s -o /tmp/resp.json -w '%{http_code}' -X "$metodo" "$BASE$ruta")
  fi
  if [ "$code" = "$esperado" ]; then OK=$((OK+1)); echo "PASS [$code] $desc"
  else FAIL=$((FAIL+1)); echo "FAIL [$code != $esperado] $desc :: $(cat /tmp/resp.json)"; fi
}

# Salud y contrato
check "GET /health responde ok"                 200 GET /health
check "GET /openapi.json disponible"            200 GET /openapi.json
check "GET / sirve la GUI"                      200 GET /

# Listar
check "GET /tasks lista tareas"                 200 GET /tasks
check "GET /tasks/ (barra final) no existe"     404 GET /tasks/

# Crear
check "POST /tasks crea tarea"                  201 POST /tasks '{"title":"Prueba QA"}'
ID=$(sed -E 's/.*"id":([0-9]+).*/\1/' /tmp/resp.json)
check "POST /tasks con done=true"               201 POST /tasks '{"title":"Ya hecha","done":true}'
check "POST /tasks título de 100 caracteres"    201 POST /tasks "{\"title\":\"$(printf 'a%.0s' {1..100})\"}"
check "POST /tasks título de 101 caracteres"    422 POST /tasks "{\"title\":\"$(printf 'a%.0s' {1..101})\"}"
check "POST /tasks título vacío"                422 POST /tasks '{"title":""}'
check "POST /tasks sin título"                  422 POST /tasks '{}'
check "POST /tasks done no booleano"            422 POST /tasks '{"title":"x","done":"quizas"}'
check "POST /tasks JSON inválido"               422 POST /tasks '{title:'

# Consultar
check "GET /tasks/{id} existente"               200 GET "/tasks/$ID"
check "GET /tasks/{id} inexistente"             404 GET /tasks/99999
check "GET /tasks/{id} no numérico"             422 GET /tasks/abc

# Actualizar
check "PATCH completar tarea"                   200 PATCH "/tasks/$ID" '{"done":true}'
check "PATCH renombrar tarea"                   200 PATCH "/tasks/$ID" '{"title":"Renombrada"}'
check "PATCH título vacío"                      422 PATCH "/tasks/$ID" '{"title":""}'
check "PATCH sin campos"                        422 PATCH "/tasks/$ID" '{}'
check "PATCH tarea inexistente"                 404 PATCH /tasks/99999 '{"done":true}'
check "PATCH id no numérico"                    422 PATCH /tasks/abc '{"done":true}'

# Eliminar
check "DELETE tarea existente"                  204 DELETE "/tasks/$ID"
check "GET tarea eliminada"                     404 GET "/tasks/$ID"
check "DELETE de nuevo (ya eliminada)"          404 DELETE "/tasks/$ID"
check "DELETE id no numérico"                   422 DELETE /tasks/abc

# Fuera del contrato
check "POST /auth/login credenciales válidas"   200 POST /auth/login '{"email":"demo@pruega.local","password":"demo1234"}'
check "POST /auth/login credenciales malas"     401 POST /auth/login '{"email":"demo@pruega.local","password":"x"}'

echo "---- $OK pasaron, $FAIL fallaron ----"
[ "$FAIL" -eq 0 ]
