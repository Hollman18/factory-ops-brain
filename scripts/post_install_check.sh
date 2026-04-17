#!/usr/bin/env bash
set -Eeuo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
CLIENT_CONFIG_ROOT="$WORKSPACE/CLIENT_CONFIG.json"
CLIENT_CONFIG_TEMPLATE="$WORKSPACE/workspace-template/CLIENT_CONFIG.json"

fail() { echo "[ERROR] $*"; exit 1; }
ok() { echo "[OK] $*"; }

[[ -f "$CLIENT_CONFIG_ROOT" || -f "$CLIENT_CONFIG_TEMPLATE" ]] || fail "No existe CLIENT_CONFIG.json"
python3 -m json.tool "${CLIENT_CONFIG_ROOT:-$CLIENT_CONFIG_TEMPLATE}" >/dev/null 2>&1 || fail "CLIENT_CONFIG.json inválido"
ok "CLIENT_CONFIG.json válido"

export DATABASE_URL="${DATABASE_URL:-}"
[[ -n "$DATABASE_URL" ]] || fail "DATABASE_URL no está configurada"
psql "$DATABASE_URL" -c "SELECT 1;" --csv -t >/dev/null 2>&1 || fail "BD no responde"
ok "Conexión a BD OK"

python3 "$WORKSPACE/analytics/schema_check.py" >/dev/null || fail "Schema incompatible"
ok "Schema check OK"

PLANTA_ID=$(python3 - <<'PY'
import json, os
paths=[os.path.expanduser('~/.openclaw/workspace/CLIENT_CONFIG.json'), os.path.expanduser('~/.openclaw/workspace/workspace-template/CLIENT_CONFIG.json')]
for p in paths:
    if os.path.exists(p):
        d=json.load(open(p))
        print(d.get('planta_id') or d.get('default_planta_id') or '')
        break
PY
)
[[ -n "$PLANTA_ID" ]] || fail "No se pudo resolver planta_id"

python3 "$WORKSPACE/analytics/db_query.py" --query-type capacity --planta-id "$PLANTA_ID" --fecha-inicio "$(date +%F)" --fecha-fin "$(date +%F)" >/dev/null || fail "db_query.py falló"
ok "db_query.py OK"

python3 "$WORKSPACE/analytics/anomaly_detector.py" --planta-id "$PLANTA_ID" >/dev/null || fail "anomaly_detector.py falló"
ok "anomaly_detector.py OK"

openclaw gateway status >/dev/null 2>&1 || fail "Gateway no disponible"
ok "Gateway status OK"

openclaw cron list >/dev/null 2>&1 || fail "No fue posible listar cron jobs"
ok "Cron list OK"

echo "Post-install check completado correctamente."
