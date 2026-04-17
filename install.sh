#!/usr/bin/env bash
set -Eeuo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log()  { echo -e "${BLUE}[INFO]${NC} $*"; }
ok()   { echo -e "${GREEN}[OK]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
err()  { echo -e "${RED}[ERROR]${NC} $*"; }

usage() {
  cat <<EOF
Uso:
  ./install.sh [flags]

Flags:
  --repo-url
  --client-name
  --db-url
  --telegram-token
  --telegram-gerente
  --telegram-supervisor
  --telegram-mantenimiento
  --telegram-calidad
  --whatsapp-token
  --planta-id
  --tz
  --api-key
  --model
  --workspace
  --non-interactive
EOF
}

REPO_URL=""
CLIENT_NAME=""
DB_URL=""
TELEGRAM_TOKEN=""
TELEGRAM_GERENTE=""
TELEGRAM_SUPERVISOR=""
TELEGRAM_MANTENIMIENTO=""
TELEGRAM_CALIDAD=""
WHATSAPP_TOKEN=""
PLANTA_ID=""
TZ_NAME=""
API_KEY=""
MODEL_NAME=""
WORKSPACE_OVERRIDE=""
NON_INTERACTIVE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo-url) REPO_URL="$2"; shift 2 ;;
    --client-name) CLIENT_NAME="$2"; shift 2 ;;
    --db-url) DB_URL="$2"; shift 2 ;;
    --telegram-token) TELEGRAM_TOKEN="$2"; shift 2 ;;
    --telegram-gerente) TELEGRAM_GERENTE="$2"; shift 2 ;;
    --telegram-supervisor) TELEGRAM_SUPERVISOR="$2"; shift 2 ;;
    --telegram-mantenimiento) TELEGRAM_MANTENIMIENTO="$2"; shift 2 ;;
    --telegram-calidad) TELEGRAM_CALIDAD="$2"; shift 2 ;;
    --whatsapp-token) WHATSAPP_TOKEN="$2"; shift 2 ;;
    --planta-id) PLANTA_ID="$2"; shift 2 ;;
    --tz) TZ_NAME="$2"; shift 2 ;;
    --api-key) API_KEY="$2"; shift 2 ;;
    --model) MODEL_NAME="$2"; shift 2 ;;
    --workspace) WORKSPACE_OVERRIDE="$2"; shift 2 ;;
    --non-interactive) NON_INTERACTIVE=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) err "Flag no reconocida: $1"; usage; exit 1 ;;
  esac
done

prompt_if_missing() {
  local var_name="$1"; local prompt_text="$2"; local secret="${3:-0}"; local current="${!var_name:-}"
  if [[ -n "$current" ]]; then return 0; fi
  if [[ "$NON_INTERACTIVE" -eq 1 ]]; then err "Falta parámetro obligatorio: $var_name"; exit 1; fi
  if [[ "$secret" -eq 1 ]]; then read -r -s -p "$prompt_text: " value; echo; else read -r -p "$prompt_text: " value; fi
  printf -v "$var_name" '%s' "$value"
}

trap 'err "Instalación falló en la línea $LINENO."' ERR
check_cmd() { command -v "$1" >/dev/null 2>&1 || { err "No se encontró el comando requerido: $1"; exit 1; }; }

log "Verificando OpenClaw..."
check_cmd openclaw
OPENCLAW_VERSION="$(openclaw --version 2>/dev/null || true)"
[[ -z "$OPENCLAW_VERSION" ]] && { err "No fue posible ejecutar 'openclaw --version'"; exit 1; }
ok "OpenClaw detectado: $OPENCLAW_VERSION"

check_cmd git; check_cmd python3; check_cmd sed; check_cmd grep; check_cmd find; check_cmd bash; check_cmd psql
if ! command -v jq >/dev/null 2>&1; then warn "jq no está instalado. Se recomienda instalarlo."; fi

if [[ -z "$REPO_URL" ]]; then
  if git -C "$(pwd)" remote get-url origin >/dev/null 2>&1; then REPO_URL="$(git -C "$(pwd)" remote get-url origin)"; else REPO_URL="/tmp/factory-ops-brain"; fi
fi

prompt_if_missing CLIENT_NAME "Nombre del cliente"
prompt_if_missing DB_URL "DATABASE_URL PostgreSQL" 1
prompt_if_missing TELEGRAM_TOKEN "Token o destino de Telegram por defecto"
prompt_if_missing PLANTA_ID "Planta ID por defecto"
prompt_if_missing TZ_NAME "Zona horaria (ej. America/Bogota)"
prompt_if_missing API_KEY "API key del modelo AI / origen analítico" 1
prompt_if_missing MODEL_NAME "Modelo AI a configurar (ej. openai/gpt-5.4)"

TELEGRAM_GERENTE="${TELEGRAM_GERENTE:-$TELEGRAM_TOKEN}"
TELEGRAM_SUPERVISOR="${TELEGRAM_SUPERVISOR:-$TELEGRAM_TOKEN}"
TELEGRAM_MANTENIMIENTO="${TELEGRAM_MANTENIMIENTO:-$TELEGRAM_TOKEN}"
TELEGRAM_CALIDAD="${TELEGRAM_CALIDAD:-$TELEGRAM_TOKEN}"

log "Clonando repo en carpeta temporal..."
TMP_DIR="$(mktemp -d /tmp/factory-ops-brain-install.XXXXXX)"
cleanup_tmp() { rm -rf "$TMP_DIR"; }
trap cleanup_tmp EXIT
if [[ -d "$REPO_URL/.git" ]]; then cp -R "$REPO_URL" "$TMP_DIR/repo"; else git clone "$REPO_URL" "$TMP_DIR/repo" >/tmp/fob-clone.log 2>&1 || { err "No fue posible clonar el repo. Revisa /tmp/fob-clone.log"; exit 1; }; fi
ok "Repo preparada en $TMP_DIR/repo"

REPO_DIR="$TMP_DIR/repo"
TEMPLATE_DIR="$REPO_DIR/workspace-template"
[[ -d "$TEMPLATE_DIR" ]] || { err "No existe workspace-template/ en el repo"; exit 1; }
REPO_VERSION="$(git -C "$REPO_DIR" rev-parse --short HEAD 2>/dev/null || echo 'unknown')"
INSTALL_DATE="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
TARGET_WORKSPACE="${WORKSPACE_OVERRIDE:-${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}}"
TARGET_CLIENT_DIR="$TARGET_WORKSPACE"
mkdir -p "$TARGET_CLIENT_DIR" "$TARGET_CLIENT_DIR/memory" "$TARGET_CLIENT_DIR/workspace-template"

log "Copiando archivos al workspace..."
cp -R "$TEMPLATE_DIR"/. "$TARGET_CLIENT_DIR/" || true
[[ -d "$REPO_DIR/skills" ]] && cp -R "$REPO_DIR/skills"/. "$TARGET_CLIENT_DIR/skills/" || true
[[ -d "$REPO_DIR/automation" ]] && cp -R "$REPO_DIR/automation"/. "$TARGET_CLIENT_DIR/automation/" || true
[[ -d "$REPO_DIR/analytics" ]] && cp -R "$REPO_DIR/analytics"/. "$TARGET_CLIENT_DIR/analytics/" || true
[[ -f "$REPO_DIR/HEARTBEAT.md" ]] && cp "$REPO_DIR/HEARTBEAT.md" "$TARGET_CLIENT_DIR/HEARTBEAT.md"
ok "Archivos copiados."

log "Creando CLIENT_CONFIG.json en raíz y template..."
cat > "$TARGET_CLIENT_DIR/CLIENT_CONFIG.json" <<EOF
{
 "client_name": "{{CLIENT_NAME}}",
 "planta_id": "{{PLANTA_ID}}",
 "timezone": "{{CLIENT_TZ}}",
 "database_url": "{{DATABASE_URL}}",
 "installed_at": "{{INSTALL_DATE}}",
 "version": "{{REPO_VERSION}}"
}
EOF
cp "$TARGET_CLIENT_DIR/CLIENT_CONFIG.json" "$TARGET_CLIENT_DIR/workspace-template/CLIENT_CONFIG.json"
ok "CLIENT_CONFIG.json creado en raíz y workspace-template."

replace_placeholders() {
  local file="$1"
  sed -i "s|{{CLIENT_NAME}}|$CLIENT_NAME|g" "$file" || true
  sed -i "s|{{PLANTA_ID}}|$PLANTA_ID|g" "$file" || true
  sed -i "s|{{CLIENT_TZ}}|$TZ_NAME|g" "$file" || true
  sed -i "s|{{DATABASE_URL}}|$DB_URL|g" "$file" || true
  sed -i "s|{{INSTALL_DATE}}|$INSTALL_DATE|g" "$file" || true
  sed -i "s|{{REPO_VERSION}}|$REPO_VERSION|g" "$file" || true
  sed -i "s|CLIENT_PLANTA_ID|$PLANTA_ID|g" "$file" || true
  sed -i "s|CLIENT_TELEGRAM_GERENTE|$TELEGRAM_GERENTE|g" "$file" || true
  sed -i "s|CLIENT_TELEGRAM_SUPERVISOR|$TELEGRAM_SUPERVISOR|g" "$file" || true
  sed -i "s|CLIENT_TELEGRAM_MANTENIMIENTO|$TELEGRAM_MANTENIMIENTO|g" "$file" || true
  sed -i "s|CLIENT_TELEGRAM_CALIDAD|$TELEGRAM_CALIDAD|g" "$file" || true
  sed -i "s|CLIENT_TZ|$TZ_NAME|g" "$file" || true
}

log "Reemplazando placeholders..."
while IFS= read -r -d '' f; do replace_placeholders "$f"; done < <(find "$TARGET_CLIENT_DIR" -type f \( -name '*.md' -o -name '*.txt' -o -name '*.json' -o -name '*.py' -o -name '*.sh' \) -print0)

log "Validando placeholders remanentes..."
UNRESOLVED=$(grep -R -n -E '\{\{[A-Z0-9_]+\}\}|CLIENT_[A-Z0-9_]+' "$TARGET_CLIENT_DIR" || true)
if [[ -n "$UNRESOLVED" ]]; then
  err "Quedaron placeholders sin resolver:"; echo "$UNRESOLVED"; exit 1
fi
ok "No quedaron placeholders críticos sin resolver."

log "Configurando ~/.openclaw/openclaw.json ..."
mkdir -p "$HOME/.openclaw"
OPENCLAW_JSON="$HOME/.openclaw/openclaw.json"
python3 - <<PY
import json, os, pathlib
p = pathlib.Path(os.path.expanduser('$OPENCLAW_JSON'))
if p.exists():
    try: data = json.loads(p.read_text())
    except Exception: data = {}
else: data = {}
data.setdefault('gateway', {})
data['gateway'].setdefault('mode', 'local')
data['gateway'].setdefault('port', 18789)
data['gateway'].setdefault('bind', 'loopback')
data['model'] = '$MODEL_NAME'
data['timezone'] = '$TZ_NAME'
data['heartbeat'] = {'enabled': True, 'source': 'HEARTBEAT.md'}
data.setdefault('channels', {})
data['channels']['telegram'] = {'default_token': '$TELEGRAM_TOKEN', 'gerente': '$TELEGRAM_GERENTE', 'supervisor': '$TELEGRAM_SUPERVISOR', 'mantenimiento': '$TELEGRAM_MANTENIMIENTO', 'calidad': '$TELEGRAM_CALIDAD'}
if '$WHATSAPP_TOKEN': data['channels']['whatsapp'] = {'token': '$WHATSAPP_TOKEN'}
p.write_text(json.dumps(data, ensure_ascii=False, indent=2))
PY
ok "openclaw.json actualizado."

log "Instalando dependencias Python..."
python3 -m pip install psycopg2-binary numpy scipy --break-system-packages >/tmp/fob-pip.log 2>&1 && ok "Dependencias Python instaladas." || { err "Falló pip. Revisa /tmp/fob-pip.log"; exit 1; }

log "Probando conexión a la BD..."
export DATABASE_URL="$DB_URL"
psql "$DATABASE_URL" -c "SELECT 1;" --csv -t >/tmp/fob-db-test.log 2>&1 && ok "Conexión PostgreSQL OK." || { err "No fue posible conectar a PostgreSQL. Revisa /tmp/fob-db-test.log"; exit 1; }

log "Ejecutando cron jobs desde automation/cron-schedules.sh ..."
CRON_SCRIPT="$TARGET_CLIENT_DIR/automation/cron-schedules.sh"
[[ -f "$CRON_SCRIPT" ]] || { err "No se encontró $CRON_SCRIPT"; exit 1; }
chmod +x "$CRON_SCRIPT"
CLIENT_PLANTA_ID="$PLANTA_ID" \
CLIENT_TELEGRAM_GERENTE="$TELEGRAM_GERENTE" \
CLIENT_TELEGRAM_SUPERVISOR="$TELEGRAM_SUPERVISOR" \
CLIENT_TELEGRAM_MANTENIMIENTO="$TELEGRAM_MANTENIMIENTO" \
CLIENT_TELEGRAM_CALIDAD="$TELEGRAM_CALIDAD" \
CLIENT_TZ="$TZ_NAME" \
"$CRON_SCRIPT" >/tmp/fob-cron.log 2>&1 && ok "Cron jobs instalados." || { err "No fue posible instalar cron jobs. Revisa /tmp/fob-cron.log"; exit 1; }

log "Arrancando gateway..."
openclaw gateway start >/tmp/fob-gateway.log 2>&1 && ok "Gateway iniciado." || { err "No se pudo iniciar el gateway. Revisa /tmp/fob-gateway.log"; exit 1; }

cat <<EOF

${GREEN}Instalación completada correctamente.${NC}

Workspace instalado en:
  $TARGET_CLIENT_DIR

Archivos de configuración del cliente:
  $TARGET_CLIENT_DIR/CLIENT_CONFIG.json
  $TARGET_CLIENT_DIR/workspace-template/CLIENT_CONFIG.json

Primer mensaje que el usuario debe enviar al agente para completar el onboarding:
--------------------------------------------------
Hola, quiero iniciar mi onboarding en Factory Ops Brain. Mi planta por defecto es $PLANTA_ID. Quiero que me respondas según mi rol y uses esta base de datos como fuente principal.
--------------------------------------------------

Verificaciones recomendadas:
1. openclaw gateway status
2. openclaw cron list
3. psql "\$DATABASE_URL" -c "SELECT 1;" --csv -t
4. python3 analytics/schema_check.py
5. python3 analytics/db_query.py --query-type capacity --planta-id "$PLANTA_ID" --fecha-inicio "$(date +%F)" --fecha-fin "$(date +%F)"
6. python3 analytics/anomaly_detector.py --planta-id "$PLANTA_ID"
7. bash scripts/post_install_check.sh
EOF
